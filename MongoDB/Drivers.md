# Drivers do MongoDB

Drivers são bibliotecas que permitem que sua aplicação fale com o MongoDB. Eles escondem os detalhes do protocolo e expõem uma API em linguagem de programação.

## O que um driver faz

- Abre conexão com o servidor ou cluster.
- Serializa e desserializa BSON.
- Gerencia pooling de conexões.
- Executa consultas, comandos, updates e aggregations.
- Trata autenticação, TLS, retry e timeouts.

## Aplicações síncronas e assíncronas

### Sync

Em aplicações síncronas, a chamada ao banco bloqueia a thread atual até a operação terminar.

Use quando:
- O fluxo da aplicação é simples.
- Você quer código direto e fácil de ler.
- A carga concorrente é moderada.
- Você já usa frameworks síncronos, como Flask tradicional, scripts, jobs e CLIs.

Exemplo de driver sync:
- `pymongo`

### Async

Em aplicações assíncronas, a operação ao banco é aguardada sem bloquear a thread principal do event loop.

Use quando:
- Você trabalha com alta concorrência.
- Sua aplicação já é orientada a `async/await`.
- Você usa frameworks assíncronos, como FastAPI, Starlette, Quart ou outros servers baseados em event loop.

Exemplo de driver async:
- `motor` (driver async oficial amplamente usado com MongoDB)

## Diferença prática

- Sync: mais simples, mas bloqueia enquanto espera a resposta do banco.
- Async: mais eficiente para muitas requisições concorrentes, mas exige `await` e organização do event loop.

## Driver sync: `pymongo`

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.exemplo
col = db.usuarios

col.insert_one({"nome": "Ana"})
usuario = col.find_one({"nome": "Ana"})
print(usuario)
```

## Driver async: `motor`

```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.exemplo
    col = db.usuarios

    await col.insert_one({"nome": "Ana"})
    usuario = await col.find_one({"nome": "Ana"})
    print(usuario)

asyncio.run(main())
```

## Quando escolher cada um

### Escolha `pymongo` se:

- Sua aplicação é síncrona.
- Você quer simplicidade.
- Você está escrevendo scripts, ETL, automações ou APIs sem `async`.

### Escolha `motor` se:

- Sua aplicação é assíncrona do início ao fim.
- Você quer manter o event loop livre enquanto espera o banco.
- Sua stack já usa `async/await` de forma nativa.

## Boas práticas

- Reutilize o cliente; não crie um novo `MongoClient` por requisição.
- Configure timeouts e pooling de acordo com o ambiente.
- Em async, use `await` em todas as operações do driver.
- Não misture sync e async no mesmo fluxo sem necessidade.

## Observação importante

- Se FastAPI, normalmente use `motor` em rotas `async def`.
- Se Flask tradicional ou script, `pymongo` costuma ser a opção mais simples.
- O banco é o mesmo, o que muda é o estilo de integração da aplicação.

## Resumo rápido

| Tipo | Driver | Característica |
| --- | --- | --- |
| Sync | `pymongo` | simples, bloqueante |
| Async | `motor` | concorrente, não bloqueante |
