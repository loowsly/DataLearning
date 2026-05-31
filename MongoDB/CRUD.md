# CRUD no MongoDB com Python

> CRUD é a base de quase tudo que você faz com dados em MongoDB.

## Fluxo rápido

| Etapa | Método Python | Resultado |
| --- | --- | --- |
| Create | `insert_one` / `insert_many` | cria documentos |
| Read | `find` / `find_one` | consulta documentos |
| Update | `update_one` / `update_many` | altera documentos |
| Delete | `delete_one` / `delete_many` | remove documentos |

## O que é CRUD

CRUD é o conjunto das quatro operações básicas usadas para manipular dados em um banco de dados:

- Create, para criar dados.
- Read, para ler dados.
- Update, para atualizar dados.
- Delete, para remover dados.

No MongoDB, essas operações são feitas sobre documentos dentro de coleções. Neste arquivo, os exemplos usam Python com a biblioteca `pymongo`.

## Conexão inicial

Antes de fazer CRUD, voce precisa conectar ao banco:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meu_banco"]
usuarios = db["usuarios"]
```

## Create

A operação de criação insere um novo documento em uma coleção.

Use `insert_one` quando quiser adicionar um único documento e `insert_many` quando quiser enviar vários de uma vez.

Exemplo:

```python
usuario = {
	"nome": "Ana",
	"email": "ana@email.com",
	"idade": 28
}

usuarios.insert_one(usuario)
```

Quando queremos inserir vários documentos de uma vez, usamos `insert_many`.

```python
usuarios.insert_many([
	{"nome": "Carlos", "email": "carlos@email.com"},
	{"nome": "Marina", "email": "marina@email.com"}
])
```

## Read

A operação de leitura busca documentos em uma coleção.

Leitura costuma ser a etapa mais frequente, então vale usar filtros e projeções para trazer só o que interessa.

Exemplo para buscar todos os documentos:

```python
for usuario in usuarios.find():
	print(usuario)
```

Exemplo com filtro:

```python
for usuario in usuarios.find({"nome": "Ana"}):
	print(usuario)
```

Exemplo para buscar apenas um documento:

```python
usuario = usuarios.find_one({"email": "ana@email.com"})
print(usuario)
```

Também é comum usar projeção para escolher quais campos retornar:

```python
for usuario in usuarios.find(
	{"idade": {"$gte": 18}},
	{"nome": 1, "email": 1, "_id": 0}
):
	print(usuario)
```

## Update

A operação de atualização altera documentos existentes.

Em geral, use `$set` para atualizar campos específicos sem reescrever o documento inteiro.

Exemplo para atualizar um único documento:

```python
usuarios.update_one(
	{"email": "ana@email.com"},
	{"$set": {"idade": 29}}
)
```

Exemplo para atualizar vários documentos:

```python
usuarios.update_many(
	{"ativo": False},
	{"$set": {"ativo": True}}
)
```

Operadores comuns de update:

- `$set` para definir ou trocar um valor.
- `$unset` para remover um campo.
- `$inc` para incrementar números.
- `$push` para adicionar itens em arrays.
- `$pull` para remover itens de arrays.

Exemplo com incremento:

```python
usuarios.update_one(
	{"nome": "Carlos"},
	{"$inc": {"idade": 1}}
)
```

## Delete

A operação de exclusão remove documentos da coleção.

Se houver risco de apagar mais do que deveria, prefira filtros bem específicos ou teste com `find` antes.

Exemplo para remover um documento:

```python
usuarios.delete_one({"email": "ana@email.com"})
```

Exemplo para remover vários documentos:

```python
usuarios.delete_many({"ativo": False})
```

## Como pensar no CRUD no MongoDB

MongoDB trabalha diretamente com documentos, então o CRUD costuma ser mais natural quando os dados já são modelados em estruturas parecidas com JSON.

O melhor fluxo costuma ser:

1. Conectar ao banco.
2. Escolher a coleção.
3. Ler ou filtrar antes de alterar.
4. Atualizar com operadores.
5. Remover com cuidado.

Pontos importantes:

- Cada documento pode ter campos diferentes.
- Consultas podem usar filtros simples ou avançados.
- Updates podem modificar campos específicos sem reescrever o documento inteiro.
- Índices ajudam a acelerar leituras e buscas.

## Exemplo completo

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["meu_banco"]
usuarios = db["usuarios"]

# Create
usuarios.insert_one({
	"nome": "Joao",
	"email": "joao@email.com",
	"idade": 22,
	"ativo": True
})

# Read
usuario = usuarios.find_one({"email": "joao@email.com"})
print(usuario)

# Update
usuarios.update_one(
	{"email": "joao@email.com"},
	{"$set": {"idade": 23}}
)

# Delete
usuarios.delete_one({"email": "joao@email.com"})
```