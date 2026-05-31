# Conexão e Connection String (MongoDB)

## Formatos comuns de connection string

- Local (sem autenticação):
  - `mongodb://localhost:27017`
- Replica set com múltiplos hosts:
  - `mongodb://host1:27017,host2:27017,host3:27017/?replicaSet=rs0`
- Atlas (SRV):
  - `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/mydb?retryWrites=true&w=majority`

Observações:
- `mongodb+srv` usa DNS SRV e requer `dnspython` disponível no ambiente (o driver tentará resolver automaticamente).
- Use query params para ajustar opções: `authSource`, `replicaSet`, `ssl=true` (ou `tls=true`), `retryWrites`, `w`, `connectTimeoutMS`, `serverSelectionTimeoutMS`.

## Boas práticas com credenciais

- Não colocar usuário/senha em código. Use variáveis de ambiente ou um secret manager.
- Exemplo com variáveis de ambiente:

```bash
export MONGO_URI="mongodb+srv://user:password@cluster0.xxxxx.mongodb.net/mydb?retryWrites=true&w=majority"
```

## Exemplo PyMongo — conectar (básico)

```python
import os
from pymongo import MongoClient

uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(uri)

db = client.get_database()  # usa nome do DB na URI se presente
print(client.server_info())  # verifica conexão (pode levantar exceptions)
```

Usar `server_info()` apenas para testes; em produção prefira `client.admin.command('ping')` ou confiar na exceção levantada ao criar o cliente quando servidores não responderem.

## Exemplo PyMongo — opções úteis

```python
client = MongoClient(
    uri,
    tls=True,  # ou ssl=True (alias)
    tlsAllowInvalidCertificates=False,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    maxPoolSize=100,
    minPoolSize=0,
    retryWrites=True
)
```

## Atlas SRV notas

- Ao usar `mongodb+srv://` não inclua portas; o driver resolve via DNS.
- Remova caracteres especiais do password ou escape/URL‑encode (ex.: `pass@word` → `pass%40word`).
- Para usar TLS/SSL, o Atlas já exige TLS; configure `tls=true` e `tlsAllowInvalidCertificates` conforme ambiente.

## Conexão com autenticação SCRAM ou X.509

- SCRAM (usuário/senha) é o método padrão do Atlas.
- X.509 (certificados) exige configuração de certificados e `tlsCAFile`, `tlsCertificateKeyFile` opções no `MongoClient`.

## Replica set e leitura/escrita

- Para preferir leitura em secundários, use `readPreference='secondaryPreferred'`.
- Para garantir durabilidade, ajuste `w='majority'` em operações de escrita ou na URI.

Exemplo de operação com write concern:

```python
from pymongo import WriteConcern
coll = db.get_collection('test', write_concern=WriteConcern(w='majority'))
coll.insert_one({'x': 1})
```

## Pooling e lifecycle

- `MongoClient` gerencia um pool de conexões; reutilize a instância `MongoClient` em toda a aplicação.
- Feche o cliente ao finalizar a aplicação: `client.close()`.

## Exemplos: conexão segura usando variáveis de ambiente

```python
import os
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError('MONGO_URI is not set')

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
except Exception as e:
    print('Erro ao conectar:', e)
    raise
```

## Depuração de problemas de conexão

- Verifique `serverSelectionTimeoutMS` para ajustar o tempo que o driver espera.
- Use `client.server_info()` ou `admin.command('ping')` para checar conectividade.
- Habilite logging do `pymongo` para obter detalhes:

```python
import logging
logging.basicConfig()
logging.getLogger('pymongo').setLevel(logging.DEBUG)
```

## Exemplo: iniciar sessão e transações (com replica set)

```python
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
with client.start_session() as session:
    with session.start_transaction():
        db.orders.insert_one({'x': 1}, session=session)
```

## Checklist rápido

- Use variáveis de ambiente para a URI.
- Reutilize `MongoClient` — não crie por operação.
- Configure `serverSelectionTimeoutMS` e `connectTimeoutMS` conforme o ambiente.
- Ajuste `maxPoolSize` para a concorrência esperada.
- Proteja credenciais com um secret manager ou `.env` fora do repositório.
