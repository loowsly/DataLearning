# Tipos de dados no MongoDB (BSON)

## Visão geral

- MongoDB usa BSON (Binary JSON) internamente - formatos binários com tipos adicionais (dates, ObjectId, Decimal128, binário, regex, etc.).
- JSON é apenas uma representação textual; BSON adiciona tipos e eficiência.

## Principais tipos BSON

- `Double` - ponto flutuante (IEEE 754). (PyMongo: `float`)
- `String` - cadeia de caracteres UTF-8. (PyMongo: `str`)
- `Object` (Embedded Document) - documento aninhado. (PyMongo: `dict`)
- `Array` - lista ordenada. (PyMongo: `list`)
- `Binary` - dados binários. (PyMongo: `bson.binary.Binary` / `bytes`)
- `ObjectId` - identificador único gerado pelo MongoDB. (PyMongo: `bson.ObjectId`)
- `Boolean` - `true`/`false`. (PyMongo: `bool`)
- `Date` - data/hora (armazenada em UTC). (PyMongo: `datetime.datetime`)
- `Null` - valor nulo. (PyMongo: `None`)
- `Regex` - expressão regular. (PyMongo: `bson.regex.Regex` ou Python `re` em consultas)
- `Int32` / `Int64` - inteiros 32/64 bits (PyMongo: `int`, armazena conforme necessário)
- `Timestamp` - tipo interno para replicação/ordenação (PyMongo: `bson.timestamp.Timestamp`)
- `Decimal128` - decimal de alta precisão (PyMongo: `bson.decimal128.Decimal128` / `decimal.Decimal`)
- `MinKey` / `MaxKey` - valores sentinela para comparações extremas
- `DBPointer` / `DBRef` - referências históricas (prefira armazenar `_id`/referências simples)
- `Javascript` - código JavaScript (raro em apps modernas)

## Notas sobre números

- PyMongo usa `int` e `float` de Python; o driver decide se precisa armazenar como `Int32`, `Int64` ou `Double`.
- Para precisão monetária, use `Decimal128` (ex.: `bson.decimal128.Decimal128(Decimal('12.34'))`).

## Mapeamento rápido (BSON ↔ PyMongo / Python)

- `ObjectId` ⇄ `bson.objectid.ObjectId`
- `Decimal128` ⇄ `bson.decimal128.Decimal128` (pode envolver `decimal.Decimal`)
- `Binary` ⇄ `bson.binary.Binary` / `bytes`
- `Date` ⇄ `datetime.datetime` (com timezone UTC preferível)
- `Regex` ⇄ `bson.regex.Regex` / Python `re` (para construção)

## Exemplo em Python (inserção e tipos)

```python
from pymongo import MongoClient
from bson import ObjectId, Binary, Decimal128
from decimal import Decimal
from datetime import datetime

client = MongoClient()
db = client.exemplo
col = db.produtos

doc = {
    "_id": ObjectId(),
    "nome": "Cafeteira",
    "preco": Decimal128(Decimal('149.90')),
    "estoque": 42,
    "tags": ["cozinha", "eletronico"],
    "meta": Binary(b"bin-data"),
    "criado_em": datetime.utcnow()
}

col.insert_one(doc)
```

## Consultas por tipo

- Usar `$type` para filtrar pelo tipo BSON:

```js
// encontrar documentos onde 'preco' é Decimal128
db.produtos.find({ preco: { $type: "decimal" } })

// em números: $type: 18 (Decimal128), 16 (Int32), 18 (Int64 is 18 depending on server), 1 (Double)
```

Exemplo PyMongo:

```python
# procurar por campos que são Decimal128
docs = col.find({"preco": {"$type": "decimal"}})
```

## Códigos numéricos `$type` úteis

- 1 - Double
- 2 - String
- 3 - Object
- 4 - Array
- 8 - Boolean
- 9 - Date
- 10 - Null
- 16 - Int32
- 18 - Int64
- 19 - Decimal128 (em algumas versões/servidores)
- 255 - Undefined (obsoleto)

(OBS: as correspondências numéricas podem variar entre versões; usar nomes (`"double"`, `"string"`, `"decimal"`) é mais legível.)

## Boas práticas e armadilhas

- Prefira `Decimal128` para valores monetários; evite `float` para dinheiro.
- Armazenar grandes blobs binários no MongoDB pode aumentar o documento rapidamente - considere GridFS para arquivos > 16MB.
- `ObjectId` contém timestamp incorporado; não dependa dele para regras de negócio sensíveis (use campo `created_at` quando precisar).
- Campos ausentes (`missing`) são diferentes de `null` - planeje consultas e índices considerando ambos.
- Ao mapear para APIs JSON, converta `ObjectId`, `Decimal128` e `datetime` para representações serializáveis (string/ISO/decimal string).

## Quando usar cada tipo

- `Embedded Document` (dict): relações 1:1 ou 1:pequenos que são sempre lidos juntos.
- `Array`: listas pequenas e ordenadas; evite arrays que cresçam indefinidamente.
- `Reference` (`ObjectId`): relações N: grandes ou compartilhadas entre muitos pais.
- `Binary`/GridFS: arquivos binários grandes ou blobs.

## Recursos

- MongoDB BSON types: https://www.mongodb.com/docs/manual/reference/bson-types/
- PyMongo docs: https://pymongo.readthedocs.io/
