# Operadores MongoDB

## Operadores de consulta

- `$in`: Um ou mais valores devem cumprir a condição.
  - Exemplo: `db.usuarios.find({ idade: { $in: [18, 21, 30] } })`
- `$nin`: Nenhum dos valores listados deve aparecer.
  - Exemplo: `db.usuarios.find({ status: { $nin: ["bloqueado", "inativo"] } })`
- `$eq`: Igualdade explícita.
  - Exemplo: `db.produtos.find({ categoria: { $eq: "livro" } })`
- `$ne`: Diferente de um valor.
  - Exemplo: `db.produtos.find({ estoque: { $ne: 0 } })`
- `$gt`: Maior que o valor informado.
  - Exemplo: `db.produtos.find({ preco: { $gt: 100 } })`
- `$gte`: Maior ou igual ao valor informado.
  - Exemplo: `db.produtos.find({ preco: { $gte: 100 } })`
- `$lt`: Menor que o valor informado.
  - Exemplo: `db.produtos.find({ preco: { $lt: 50 } })`
- `$lte`: Menor ou igual ao valor informado.
  - Exemplo: `db.produtos.find({ preco: { $lte: 50 } })`
- `$and`: Todas as condições devem ser verdadeiras.
  - Exemplo: `db.pedidos.find({ $and: [{ status: "aberto" }, { total: { $gt: 100 } }] })`
- `$or`: Pelo menos uma condição deve ser verdadeira.
  - Exemplo: `db.pedidos.find({ $or: [{ status: "aberto" }, { status: "pendente" }] })`
- `$not`: Inverte a condição.
  - Exemplo: `db.usuarios.find({ nome: { $not: /admin/i } })`
- `$exists`: Verifica se o campo existe.
  - Exemplo: `db.usuarios.find({ telefone: { $exists: true } })`
- `$regex`: Pesquisa por expressão regular.
  - Exemplo: `db.usuarios.find({ nome: { $regex: /^a/i } })`
- `$elemMatch`: Um elemento do array deve atender a múltiplas condições.
  - Exemplo: `db.posts.find({ comentarios: { $elemMatch: { autor: "Ana", curtidas: { $gte: 5 } } } })`
- `$all`: O array deve conter todos os valores informados.
  - Exemplo: `db.posts.find({ tags: { $all: ["mongodb", "python"] } })`
- `$size`: O array deve ter tamanho exato.
  - Exemplo: `db.posts.find({ tags: { $size: 3 } })`
- `$type`: O campo deve ser de um tipo específico.
  - Exemplo: `db.logs.find({ criado_em: { $type: "date" } })`

## Operadores de atualização

- `$set`: Define ou atualiza um campo.
  - Exemplo: `db.usuarios.updateOne({ _id: id }, { $set: { nome: "Maria" } })`
- `$unset`: Remove um campo.
  - Exemplo: `db.usuarios.updateOne({ _id: id }, { $unset: { telefone: "" } })`
- `$inc`: Incrementa um valor numérico.
  - Exemplo: `db.produtos.updateOne({ _id: id }, { $inc: { estoque: -1 } })`
- `$mul`: Multiplica um valor numérico.
  - Exemplo: `db.produtos.updateOne({ _id: id }, { $mul: { preco: 1.1 } })`
- `$rename`: Renomeia um campo.
  - Exemplo: `db.usuarios.updateOne({ _id: id }, { $rename: { nome_completo: "nome" } })`
- `$min`: Só atualiza se o novo valor for menor.
  - Exemplo: `db.metricas.updateOne({ _id: id }, { $min: { menor_valor: 10 } })`
- `$max`: Só atualiza se o novo valor for maior.
  - Exemplo: `db.metricas.updateOne({ _id: id }, { $max: { maior_valor: 99 } })`
- `$push`: Adiciona item ao final de um array.
  - Exemplo: `db.posts.updateOne({ _id: id }, { $push: { tags: "async" } })`
- `$addToSet`: Adiciona item apenas se ele ainda não existir no array.
  - Exemplo: `db.posts.updateOne({ _id: id }, { $addToSet: { tags: "mongodb" } })`
- `$pop`: Remove o primeiro ou o último item do array.
  - Exemplo: `db.posts.updateOne({ _id: id }, { $pop: { tags: 1 } })`
- `$pull`: Remove itens do array que atendem à condição.
  - Exemplo: `db.posts.updateOne({ _id: id }, { $pull: { tags: "velho" } })`
- `$pullAll`: Remove uma lista de valores do array.
  - Exemplo: `db.posts.updateOne({ _id: id }, { $pullAll: { tags: ["x", "y"] } })`
- `$currentDate`: Define a data/hora atual.
  - Exemplo: `db.usuarios.updateOne({ _id: id }, { $currentDate: { atualizado_em: true } })`
- `$setOnInsert`: Define o valor apenas quando o documento é inserido via upsert.
  - Exemplo: `db.usuarios.updateOne({ email: "a@a.com" }, { $setOnInsert: { criado_em: new Date() } }, { upsert: true })`

## Operadores de agregação comuns

- `$match`: Filtra documentos na pipeline.
  - Exemplo: `[{ $match: { status: "ativo" } }]`
- `$group`: Agrupa documentos e calcula agregados.
  - Exemplo: `[{ $group: { _id: "$categoria", total: { $sum: 1 } } }]`
- `$project`: Seleciona e transforma campos.
  - Exemplo: `[{ $project: { nome: 1, _id: 0 } }]`
- `$sort`: Ordena resultados.
  - Exemplo: `[{ $sort: { criado_em: -1 } }]`
- `$limit`: Limita a quantidade de resultados.
  - Exemplo: `[{ $limit: 10 }]`
- `$skip`: Pula documentos no resultado.
  - Exemplo: `[{ $skip: 20 }]`
- `$lookup`: Faz junção entre coleções.
  - Exemplo: `[{ $lookup: { from: "authors", localField: "author_id", foreignField: "_id", as: "author" } }]`
- `$unwind`: Desfaz arrays em documentos individuais.
  - Exemplo: `[{ $unwind: "$tags" }]`


## Exemplo em PyMongo

```python
from pymongo import MongoClient

client = MongoClient()
db = client.exemplo
col = db.usuarios

# consulta com $in
usuarios = list(col.find({"idade": {"$in": [18, 21, 30]}}))

# atualização com $set e $inc
col.update_one({"email": "ana@example.com"}, {"$set": {"nome": "Ana"}, "$inc": {"logins": 1}})
```