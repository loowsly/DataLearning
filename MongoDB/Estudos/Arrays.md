# Arrays em MongoDB

Arrays são tipos essenciais em documentos BSON. Aqui estão comportamentos, operadores, índices e exemplos práticos.

## Características

- Arrays são ordenados e podem conter tipos mistos.
- Tamanho do array contribui para o tamanho do documento (limite 16MB).
- Arrays grandes e de crescimento ilimitado causam problemas de performance e armazenamento.

## Índices multichave

- MongoDB cria índices multichave automaticamente quando se indexa um campo que contém um array.
- Cada elemento do array é indexado separadamente, o que pode multiplicar entradas no índice.

## Operadores úteis

- `$push`, `$pop`, `$addToSet`, `$pull`, `$pullAll` - modificar arrays
- `$elemMatch` - consultar por elemento que satisfaça múltiplas condições
- `$size` - filtrar por tamanho do array
- `$slice` - projetar parte do array
- Operador posicional `$` e `arrayFilters` para atualizar elementos específicos

## Boas práticas

- Evite arrays que cresçam sem limites; prefira coleções relacionadas quando cardinalidade for alta.
- Use `$addToSet` para evitar duplicatas quando apropriado.
- Evite indexar arrays com milhares de elementos.

## Exemplos PyMongo

```python
from pymongo import MongoClient

client = MongoClient()
db = client.exemplo
col = db.posts

post = {
    "titulo": "Meu post",
    "tags": ["python", "mongodb"],
    "comentarios": [
        {"autor": "Ana", "texto": "bom post"}
    ]
}
col.insert_one(post)

# Adicionar tag
col.update_one({"titulo": "Meu post"}, {"$addToSet": {"tags": "async"}})

# Atualizar texto do primeiro comentário por posição
col.update_one({"comentarios.autor": "Ana"}, {"$set": {"comentarios.$.texto": "ótimo post"}})

# Buscar posts com ao menos 2 tags
list(col.find({"tags": {"$size": 2}}))

# Encontrar por elemento com múltiplas condições
list(col.find({"comentarios": {"$elemMatch": {"autor": "Ana", "texto": /ób/}}}))
```