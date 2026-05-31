# Relações entre documentos no MongoDB


## Tipos de relação

- 1:1 — duas entidades relacionadas de maneira exclusiva (ex.: usuário → perfil).
- 1:N — uma entidade possui muitas entidades filhas (ex.: post → comentários).
- N:N — entidades relacionadas mutuamente (ex.: livros ↔ autores, quando múltiplos autores por livro).

## Decisão: Embedding vs Referencing

Usar embedding quando:
- A relação for 1:1 ou 1:pequenos.
- Os dados forem lidos juntos e tiverem baixa taxa de crescimento.
- Operações atômicas em todo o agregado.

Usar referencing quando:
- A cardinalidade for alta ou crescer indefinidamente.
- Subdocumentos forem compartilhados entre muitos pais.
- For necessário acessar o subdocumento independentemente do pai.

Resumo rápido:
- Embed = leituras rápidas, menos joins, tamanho limitado.
- Reference = melhor para escalabilidade e compartilhamento, requer joins/`$lookup`.

## Padrões por relação

1:1
- Embedding simples ou referenciar via `_id` se o subobjeto crescer ou precisar ser acessado isoladamente.

1:N
- Se N for pequeno e contido, embed (array de subdocumentos).
- Se N crescer sem limite, mover para coleção separada e referenciar com `parent_id`.

N:N
- Array de refs em ambos os lados (somente se arrays permanecerem pequenos).
- Coleção de ligação (join table) quando os conjuntos forem grandes ou consultas por ambos os lados forem frequentes.

## Exemplo 1: 1:1 — embedding e referência

Embedding (perfil dentro do usuário):

```python
users.insert_one({
    "nome": "Marina",
    "perfil": {"bio": "Dev", "twitter": "@m"}
})
```

Referência (perfil separado):

```python
pid = profiles.insert_one({"bio": "Dev"}).inserted_id
users.insert_one({"nome": "Marina", "profile_id": pid})
```

## Exemplo 2: 1:N — comentários

Embedding (quando comentários são poucos):

```python
posts.insert_one({"titulo": "X", "comentarios": [{"autor":"A","texto":"ok"}]})
```

Referência (quando muitos comentários):

```python
post_id = posts.insert_one({"titulo": "X"}).inserted_id
comments.insert_many([
    {"post_id": post_id, "autor": "A", "texto": "ok"},
    {"post_id": post_id, "autor": "B", "texto": "bom"}
])
```

Consulta para buscar post com comentários via aggregation `$lookup`:

```python
pipeline = [
    {"$match": {"_id": post_id}},
    {"$lookup": {
        "from": "comments",
        "localField": "_id",
        "foreignField": "post_id",
        "as": "comments"
    }}
]
post_with_comments = list(posts.aggregate(pipeline))[0]
```

## Exemplo 3: N:N — tags por post

Array de refs (quando poucas tags por post):

```python
posts.insert_one({"titulo": "Y", "tag_ids": [tag1, tag2]})
```

Coleção de relacionamento (escala):

```python
post_tags.insert_one({"post_id": p, "tag_id": t})
# Buscar posts por tag via aggregation ou index em post_tags
```

## Joins e `$lookup`

- `$lookup` permite "join" entre coleções no servidor via aggregation framework.
- Para performance, assegure índices em campos usados (`foreignField`, `localField`).
- Use `pipeline` dentro do `$lookup` para filtrar/projetar antes de retornar.

Exemplo `$lookup` com `pipeline`:

```python
pipeline = [
    {"$lookup": {
        "from": "authors",
        "let": {"aid": "$author_id"},
        "pipeline": [
            {"$match": {"$expr": {"$eq": ["$_id", "$$aid"]}}},
            {"$project": {"nome": 1, "_id": 0}}
        ],
        "as": "author"
    }},
    {"$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}}
]
```

## Consistência, transações e operações atômicas

- Operações em um único documento são atômicas — modelar agregados como documentos pode evitar transações.
- Use transações (`with client.start_session(): ...`) quando precisar de atomicidade entre múltiplas coleções.

Exemplo de transação em PyMongo:

```python
with client.start_session() as s:
    with s.start_transaction():
        oid = orders.insert_one(order_doc, session=s).inserted_id
        payments.insert_one({"order_id": oid, ...}, session=s)
```

## Deleção em cascata e limpeza

- MongoDB não faz cascata automaticamente. Estratégias:
  - Deleção manual em código (após remover pai, remover filhos).
  - Change Streams para reagir a eventos e sincronizar.
  - Soft delete com `deleted_at` e limpeza periódica.

## Denormalização e cópias derivadas

- Denormalizar (copiar campos) pode acelerar leituras, evitando joins; mantenha processos para reconciliar dados quando necessário.
- Usar Change Streams ou jobs agendados para propagar mudanças.

## Performance e índices

- Sempre indexe campos de referência usados em `find` ou `$lookup`.
- Evite arrays enormes de refs — índices multichave multiplicam entradas.
- Projete queries e crie índices compostos para padrões de busca mais comuns.