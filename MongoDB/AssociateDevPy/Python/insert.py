from pymongo import MongoClient
import os
import dotenv as env

env.load_dotenv()
uri = os.getenv("uri")


client = MongoClient(uri)
db = client.python
users = db.users


# Insert One

new_user = {
    "name": "Leoncio",
    "age": 18,
    "endereco": {
        "street": "Rua Brasil",
        "number": 98,
        "city": "Bálsamo"
    }
}

insert = users.insert_one(new_user)
insert_id = insert.inserted_id
result = print(f"New user ID: {insert_id}")

# Insert Many

new_users = [
        {
        "name": "Leoncio",
        "age": 18,
        "endereco": {
            "street": "Rua Brasil",
            "number": 98,
            "city": "Bálsamo"
        }
    },
    {
        "name": "Mariana",
        "age": 21,
        "endereco": {
            "street": "Avenida São Paulo",
            "number": 120,
            "city": "Mirassol"
        }
    },
    {
        "name": "Carlos",
        "age": 25,
        "endereco": {
            "street": "Rua das Flores",
            "number": 45,
            "city": "São José do Rio Preto"
        }
    },
    {
        "name": "Ana Clara",
        "age": 19,
        "endereco": {
            "street": "Rua Amazonas",
            "number": 77,
            "city": "Bálsamo"
        }
    },
    {
        "name": "Rafael",
        "age": 30,
        "endereco": {
            "street": "Rua Minas Gerais",
            "number": 210,
            "city": "Tanabi"
        }
    },
    {
        "name": "Juliana",
        "age": 22,
        "endereco": {
            "street": "Avenida Brasil",
            "number": 555,
            "city": "Votuporanga"
        }
    },
    {
        "name": "Pedro",
        "age": 17,
        "endereco": {
            "street": "Rua Paraná",
            "number": 89,
            "city": "Bálsamo"
        }
    },
    {
        "name": "Fernanda",
        "age": 28,
        "endereco": {
            "street": "Rua Goiás",
            "number": 340,
            "city": "Catanduva"
        }
    },
    {
        "name": "Lucas",
        "age": 20,
        "endereco": {
            "street": "Rua Sete de Setembro",
            "number": 12,
            "city": "Mirassol"
        }
    },
    {
        "name": "Beatriz",
        "age": 24,
        "endereco": {
            "street": "Rua XV de Novembro",
            "number": 150,
            "city": "São José do Rio Preto"
        }
    }
]


insertm = users.insert_many(new_users)
insertm_id = insertm.inserted_ids
result = print(f"New user ID: {insertm_id}\n")



client.close()