

import os
import sys
from pprint import pprint
from pymongo import *
import dotenv as env

env.load_dotenv()
URI = os.getenv('uri')
client = MongoClient(URI)


def connect(uri):
    try:
        client.admin.command('ping')
        return client
    except Exception as e:
        print('Não foi possível conectar ao MongoDB em', uri)
        print('Erro:', e)
        return None


def criar_index(DB):
    print('\nCriando índices de exemplo...')

    users = DB.users

    users.create_index([('email', 1)], name='idx_users_email')

    print('Índices criados. Listando índices da coleção users:')
    pprint(list(users.list_indexes()))


def explain(DB):
    print('\nExecutando explain() em queries de exemplo...')

    users = DB.users

    print('\nQuery: users.find({email: \"a@a.com\"})')
    res = users.find({'email': 'a@a.com'})
    try:
        plan = users.find({'email': 'a@a.com'}).explain()
        pprint(plan['queryPlanner'])
        print('executionStats: nReturned=', plan.get('executionStats', {}).get('nReturned'))
    except Exception as e:
        print('explain() não pôde ser executado:', e)


def data_mock(DB):
    print('\nInserindo documentos de exemplo')
    users = DB.users
    orders = DB.orders

    users.insert_one({'email': 'a@a.com', 'name': 'Alice'})
    for i in range(3):
        orders.insert_one({'user_id': 123, 'total': 10 * (i + 1), 'created_at': None})


def main():
    client = connect(URI)
    if client is None:
        print('\nAbortando')
        sys.exit(1)

    DB = client["python"]

    criar_index(DB)
    data_mock(DB)
    explain(DB)

    print('\nDemonstração finalizada.')


if __name__ == '__main__':
    main()
