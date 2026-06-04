# Índices no MongoDB

## Por que usar índices

- Acelerar consultas (`find`, `sort`, `aggregate` com `$match`/`$sort`).
- Reduzir número de documentos examinados (menos leitura e CPU).
- Suportar unicidade e restrições (índices únicos).

Sem índices adequados, o MongoDB faz *collection scan* (varre toda a coleção).

## Tipos comuns de índices

- Single field index: índice em um campo simples (ex.: `{ user_id: 1 }`).
- Compound index: índice composto por vários campos (ex.: `{ user_id: 1, created_at: -1 }`).
- Multikey index: criado automaticamente quando um campo é um array; indexa cada elemento.
- Text index: para buscas por texto (`$text`) com suporte a stemming e idiomas.
- Hashed index: índice hash (útil para sharding por hashed shard key).
- TTL index: índice com `expireAfterSeconds` para remover documentos automaticamente.
- Unique index: garante unicidade do valor do campo.
- Partial index: aplica‑se somente aos documentos que casam uma expressão (`partialFilterExpression`).
- Sparse index: indexa somente documentos que contenham o campo (desaconselhado em muitos casos, prefira `partial`).
- Wildcard index: `{$**: 1}` para indexar campos dinâmicos ou desconhecidos.

## Criando índices (shell)

```js
// Single field
db.users.createIndex({ email: 1 })

// Compound
db.orders.createIndex({ user_id: 1, created_at: -1 })

// Text
db.articles.createIndex({ title: "text", body: "text" })

// Hashed
db.sessions.createIndex({ session_id: "hashed" })

// TTL (remove documentos 3600s após o campo 'created_at')
db.tokens.createIndex({ created_at: 1 }, { expireAfterSeconds: 3600 })

// Partial
db.products.createIndex({ price: 1 }, { partialFilterExpression: { price: { $exists: true } } })
```

## Criando índices (PyMongo)

```python
import pymongo

client = MongoClient()
db = client.exemplo

# Single field
db.users.create_index([('email', ASCENDING)], name='email_idx')

# Compound
db.orders.create_index([('user_id', ASCENDING), ('created_at', DESCENDING)], name='orders_user_date')

# Text
db.articles.create_index([('title', TEXT), ('body', TEXT)], name='articles_text')

# Hashed
db.sessions.create_index([('session_id', HASHED)])

# TTL
db.tokens.create_index([('created_at', ASCENDING)], expireAfterSeconds=3600)

# Partial
db.products.create_index([('price', ASCENDING)], partialFilterExpression={'price': {'$exists': True}})
```

## Verificar índices

```js
db.collection.getIndexes()
db.collection.stats().indexSizes
```

Em `pymongo`:

```python
list(db.users.list_indexes())
```

## Como escolher índices

- Modele para suas consultas frequentes (consultas e patterns de sort).
- Prefira índices compostos que cubram a consulta completa (`find` + `sort`).
- Orden dos campos em índices compostos importa: `{a:1,b:1}` serve para queries em `a` e em `a,b`.
- Evite criar índices em demasiados campos (custo de escrita e espaço).

## Índices multichave e arrays

- Índices em campos que são arrays geram entradas para cada elemento do array.
- Cuidado: arrays grandes podem inflar o índice (explode em número de entradas).

## Index usage e `explain()`

Use `explain()` para entender se a query usa índice:

```js
db.orders.find({ user_id: 123 }).explain('executionStats')
```

Procure por `IXSCAN` no plano - indica uso de índice; `COLLSCAN` indica varredura completa.

## Boas práticas

- Criar índices com base em evidências (query patterns, `explain`, profiler).
- Monitorar impacto de índices nas operações de escrita.
- Usar `partial` e `sparse` para reduzir tamanho quando fizer sentido.
- Usar índices compostos para cobrir consultas e evitar fetch de documento quando possível.
- Evitar índices redundantes (um índice prefixo cobre queries que usam prefixo correspondente).
- Em produção, criar índices em background (antigo) ou usar `createIndex` sem interromper serviço; em versões recentes o build é online para a maior parte dos casos.

## Considerações de armazenamento e custo

- Índices ocupam espaço em disco/RAM: cada índice aumenta uso de armazenamento e memória do working set.
- Recalcule cardinalidades e tamanho do índice quando projetar escalabilidade.

## Índices especiais

- Wildcard index: útil para documentos semi‑estruturados com muitos campos dinâmicos.
- Collation: índice com collation permite ordenação e comparações por idioma/locale.
- Unique index: use para garantir unicidade e integridade (por exemplo `email`).

## Remover índice

```js
db.users.dropIndex('email_idx')
```

## Exemplo prático de produção

- Identifique a query mais custosa com o profiler.
- Rode `explain()` para ver se scan é `COLLSCAN`.
- Se necessário, crie índice composto que cubra `filter` + `sort`.
- Meça impacto nas escritas e ajuste.