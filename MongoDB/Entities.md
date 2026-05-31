# Entidades e agregados no MongoDB

## O que é uma entidade

- Entidade: objeto do domínio com identidade própria (campo `_id`).
- Em bancos relacionais, entidades mapeiam para linhas; em MongoDB, uma entidade costuma mapear para um documento (ou conjunto de documentos relacionados).

## Agregados e boundaries

- Agregado: conjunto de objetos que devem ser tratados como uma unidade de consistência e que têm uma raiz (aggregate root).
- No MongoDB, é comum armazenar um agregado inteiro como um documento (embedding) quando o agregado é pequeno e as operações ocorrem majoritariamente sobre ele.
- Defina claramente limites de agregados para decidir entre embedding e referências.

## Estratégias de mapeamento entidade → documento

1. Documento por entidade (1:1): cada entidade vira um documento na coleção correspondente.
2. Agregado embutido: todas as entidades do agregado são embutidas no documento raiz.
3. Entidade com referência: entidade separada em outra coleção referenciada por `_id`.
4. Coleção de relacionamento: para N:N ou quando buscas por ambos os lados são frequentes.

## Identificadores

- Use `ObjectId` por padrão (gerado automaticamente), ou UUIDs se precisar de IDs gerados no cliente.
- `_id` é único por coleção; para outras restrições use índices únicos.

## Polimorfismo e discriminators

- Para entidades polimórficas (mesma coleção com tipos diferentes), inclua um campo `type`/`kind` para discriminar e facilitar consultas/indices.

Exemplo:

```json
{ "_id": ..., "type": "carro", "marca": "Fiat", "portas": 4 }
{ "_id": ..., "type": "moto", "marca": "Honda", "cilindradas": 160 }
```

## Validação de esquema (JSON Schema)

- MongoDB suporta validação de documento via `validator` (JSON Schema). Use para garantir contratos mínimos.

Exemplo de criação de coleção com validator (PyMongo):

```python
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

client = MongoClient()
db = client.exemplo
validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["nome", "email"],
        "properties": {
            "nome": {"bsonType": "string"},
            "email": {"bsonType": "string", "pattern": "^.+@.+$"},
            "idade": {"bsonType": ["int", "null"]}
        }
    }
}
try:
    db.create_collection("usuarios", validator=validator)
except CollectionInvalid:
    db.command({
        "collMod": "usuarios",
        "validator": validator,
        "validationLevel": "moderate"
    })
```

- `validationLevel`: `off` | `moderate` | `strict` — escolha conforme maturidade do dado.

## Padrões de versionamento e migração

- Adicione campos `schema_version` ou `version` quando precisar migrar documentos gradualmente.
- Faça migrações online (lazy migration) convertendo documentos quando lidos ou via scripts batch.

## Eventos e histórico

- Para rastrear mudanças, mantenha `created_at`, `updated_at` e, se necessário, uma coleção de audit logs.
- Change Streams podem ser usados para propagar eventos e construir pipelines de sincronização.

## Exemplo prático: modelando `Order` como agregado

- Requisitos: ordem com itens, pagamentos e status; consultas frequentes por ordem e por usuário.

Opção A — Embedding do agregado (bom se itens por ordem forem limitados):

```json
{
  "_id": ObjectId(...),
  "user_id": ObjectId(...),
  "items": [ {"product_id": ..., "qty": 2, "price": 19.9} ],
  "status": "created",
  "total": 39.8,
  "created_at": ISODate(...)
}
```

Opção B — Order + OrderItems em coleções separadas (quando muitos itens por pedido):

- `orders` (order metadata)
- `order_items` (cada item com `order_id`)

## Consultas e índices recomendados

- Index em `_id` (automático).
- Index em campos de busca frequente: `user_id`, `status`, `created_at`.
- Índices compostos para consultas combinadas (ex.: `{user_id:1, created_at:-1}`).

## Consistência e transações

- Use transações para operações que toquem múltiplas coleções/entidades e precisam ser atômicas.
- Para a maior parte dos cenários, modelar agregados como documentos atômicos reduz a necessidade de transações.

## Soft delete vs hard delete

- Soft delete: marcar `deleted_at` para manter histórico e evitar inconsistências em referências.
- Hard delete: remover fisicamente; combine com limpeza periódica de coleções relacionadas se necessário.

## Boas práticas

- Modele em função das consultas: priorize as consultas mais frequentes e críticas.
- Mantenha limites razoáveis de tamanho de documento e níveis de aninhamento.
- Documente contratos entre coleções (quem referencia quem).
- Automatize validações e migrações usando `schema_version` e scripts determinísticos.

## Exemplo PyMongo curto (Orders embed)

```python
from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.exemplo
orders = db.orders

order = {
    "user_id": 123,
    "items": [
        {"product_id": 1, "qty": 2, "price": 9.9},
        {"product_id": 2, "qty": 1, "price": 19.9}
    ],
    "status": "created",
    "total": 39.7,
    "created_at": datetime.utcnow(),
    "schema_version": 1
}

orders.insert_one(order)
```
