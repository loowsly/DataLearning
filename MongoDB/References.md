# Referências entre documentos (Referencing)

## Por que usar referências

- Quando um subdocumento é grande ou cresce independentemente do pai.
- Quando o mesmo subdocumento é compartilhado por muitos documentos (normalização).
- Quando a cardinalidade é alta (1:N grande) e embedding causaria documentos muito grandes.
- Quando atualizações frequentes ao subdocumento tornariam o embutimento custoso.

## Padrões comuns

- Referência manual: armazenar o `_id` do documento relacionado (ex.: `author_id`).
- Array de referências: armazenar uma lista de `_id` (ex.: `tag_ids`).
- `DBRef`: formato legado que inclui coleção e banco além do `_id`.
- `$lookup`: operação de agregação no servidor que realiza um "join" entre coleções.
- `$graphLookup`: lookup recursivo para hierarquias (árvores/graphs).

## DBRef vs referência manual

- `DBRef` tem forma padronizada: `{ "$ref": "colecao", "$id": ObjectId(...), "$db": "nome" }`.
- Drivers modernos (como `pymongo`) não exigem `DBRef`; armazenar `_id` e fazer `$lookup`/queries é mais simples.
- Use `DBRef` apenas se precisar de metadados de coleção/banco junto com a referência por algum motivo específico.

## Exemplo: referência manual (autor → livros)

```python
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
db = client.exemplo
authors = db.authors
books = db.books

# Inserir autor
author_id = authors.insert_one({"nome": "Paulo Silva"}).inserted_id

# Inserir livro referenciando o autor
book = {
    "titulo": "Noções de MongoDB",
    "author_id": author_id,
    "ano": 2024
}
books.insert_one(book)

# Buscar livros e popular client-side (consulta manual)
for b in books.find({}):
    a = authors.find_one({"_id": b['author_id']})
    print(b['titulo'], "—", a['nome'])
```

## Populando no servidor com `$lookup`

```python
pipeline = [
    {
        "$lookup": {
            "from": "authors",
            "localField": "author_id",
            "foreignField": "_id",
            "as": "author"
        }
    },
    {"$unwind": {"path": "$author", "preserveNullAndEmptyArrays": True}}
]

for doc in books.aggregate(pipeline):
    print(doc['titulo'], '-', doc.get('author', {}).get('nome'))
```

Vantagens do `$lookup`:
- Executado no servidor, reduz múltiplas viagens cliente→servidor.
- Pode ser combinado com `pipeline` para projeções/filtragens adicionais.

Limitações:
- `$lookup` pode ser custoso em coleções muito grandes; indexe os campos usados (ex.: `_id`, `author_id`).
- Joins complexos em grande escala exigem cuidado com memória e uso de `allowDiskUse` se necessário.

## Muitos‑para‑muitos (N:N)

- Opção A: array de `ObjectId` em cada lado (ex.: `book.tag_ids = [id1, id2]`).
- Opção B: coleção de relacionamento (join table) que contém pares `{book_id, tag_id}` quando consultas por ambos os lados são frequentes.

Exemplo: buscar livros por `tag_id` usando índice em `tag_ids`:

```python
list(books.find({"tag_ids": some_tag_id}))
```

## Consistência e transações

- Operações envolvendo múltiplos documentos (ex.: criar autor e livro vinculado) podem exigir transações para garantir consistência.
- Use transações em replica sets e clusters configurados para isso:

```python
with client.start_session() as s:
    with s.start_transaction():
        aid = authors.insert_one({"nome": "Novo"}, session=s).inserted_id
        books.insert_one({"titulo": "X", "author_id": aid}, session=s)
```

## Cascata e deleção

- MongoDB não aplica cascata automática ao deletar — escolha uma estratégia:
  - Aplicar deleção manual (deletar dependentes em código ou via `delete_many`).
  - Usar triggers (Change Streams) para reagir a mudanças e propagar deleções.
  - Projetar para tolerar referências órfãs e limpar periodicamente.

Exemplo simples de deleção manual:

```python
# deletar autor e livros relacionados
aid = ObjectId("...")
authors.delete_one({"_id": aid})
books.delete_many({"author_id": aid})
```

## Performance e índices

- Indexe os campos de referência (ex.: `author_id`) para acelerar joins e buscas por relações.
- Evite arrays de refs muito grandes — índices multichave podem explodir em entradas.

## Quando preferir embedding

- Relações 1:1 ou 1:pequenos que são sempre consultadas junto são bons candidatos para embedding.
- Embedding reduz a necessidade de joins e melhora latência de leitura.

## Casos avançados

- `$graphLookup` para recorrer hierarquias (ex.: organogramas): cuidado com limites de profundidade e performance.
- `lookup` com `let`/`pipeline` permite transformações complexas durante o join.
