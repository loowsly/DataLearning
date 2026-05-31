# Documentos em MongoDB

Documentos são a unidade primária do MongoDB - essencialmente objetos/`dict` com pares `chave: valor`.

## `_id` e identidade

- Todo documento tem um campo `_id` único na coleção. Se não for fornecido, o driver (ex.: PyMongo) gera um `ObjectId`.
- `_id` é o campo principal usado para identidade e é automaticamente indexado.

## Atomicidade e transações

- Operações em um único documento são atômicas.
- Para alterações que envolvem múltiplos documentos/coleções, use transações (disponíveis em replica sets e clusters configurados).

## Tamanho máximo e estruturas grandes

- Limite: 16 MB por documento. Para arquivos maiores, use GridFS.
- Prefira embedding para relações 1:1 ou 1:pequenos; use referências para 1:N grandes.

## Atualizações comuns

- `$set` - definir/atualizar campos
- `$unset` - remover campos
- `$inc` - incrementar números
- `$push` / `$addToSet` / `$pull` - manipular arrays
- `upsert=True` - criar documento se não existir

Exemplo PyMongo:

```python
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient()
db = client.exemplo
col = db.usuarios

# Upsert: cria se não existir
col.update_one({"email": "joao@example.com"}, {"$set": {"nome": "João"}}, upsert=True)

# Remover campo
col.update_one({"_id": ObjectId("605c...")}, {"$unset": {"telefone": ""}})

# Incrementar
col.update_one({"email": "joao@example.com"}, {"$inc": {"logins": 1}})
```

## Projeção e desempenho

- Projete apenas campos necessários usando segundo argumento em `find` ou `projection` para reduzir transferência de dados.
- Operações de leitura devem usar índices sempre que possível.