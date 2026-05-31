# Comandos básicos do MongoDB em Python


## Conexão inicial

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meu_banco"]
usuarios = db["usuarios"]
```

## Principais operações

| Operação | Método em Python | Objetivo |
| --- | --- | --- |
| Criar um documento | `insert_one` | inserir um registro |
| Criar vários documentos | `insert_many` | inserir em lote |
| Ler documentos | `find` | retornar vários resultados |
| Ler um documento | `find_one` | retornar o primeiro match |
| Atualizar um documento | `update_one` | alterar um item específico |
| Atualizar vários documentos | `update_many` | alterar vários itens |
| Remover um documento | `delete_one` | apagar um item específico |
| Remover vários documentos | `delete_many` | apagar vários itens |

## Inserir documentos

```python
usuarios.insert_one({
	"nome": "Ana",
	"email": "ana@email.com",
	"idade": 28
})

usuarios.insert_many([
	{"nome": "Carlos", "email": "carlos@email.com"},
	{"nome": "Marina", "email": "marina@email.com"}
])
```

## Consultar documentos

```python
for usuario in usuarios.find():
	print(usuario)

for usuario in usuarios.find({"nome": "Ana"}):
	print(usuario)

usuario = usuarios.find_one({"email": "ana@email.com"})
print(usuario)
```

## Filtrar e projetar

```python
for usuario in usuarios.find(
	{"idade": {"$gte": 18}},
	{"nome": 1, "email": 1, "_id": 0}
):
	print(usuario)
```

## Atualizar documentos

```python
usuarios.update_one(
	{"email": "ana@email.com"},
	{"$set": {"idade": 29}}
)

usuarios.update_many(
	{"ativo": False},
	{"$set": {"ativo": True}}
)
```

## Remover documentos

```python
usuarios.delete_one({"email": "ana@email.com"})
usuarios.delete_many({"ativo": False})
```

## Consultas úteis

```python
usuarios.count_documents({"ativo": True})
usuarios.distinct("cidade")
usuarios.find_one_and_update(
	{"nome": "Carlos"},
	{"$inc": {"idade": 1}}
)
```