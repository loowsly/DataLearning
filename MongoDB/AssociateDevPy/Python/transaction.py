from pymongo import MongoClient
import os
import dotenv as env

env.load_dotenv()
uri = os.getenv("uri")

#connection
client = MongoClient(uri,maxIdleTimeMS=30000)
#set database
db = client.python
#set collection for users
users = db.users
#set collection for transfers
transfers = db.transfers

def callback(
        session,
        transfer_id=None,
        id_receiver=None,
        id_sender=None,
        amount=None
):
    
    transfer = {
        'transfer_id': transfer_id,
        'to_acc': id_receiver,
        'from_acc': id_sender,
        'amount':amount
    }

    # edit account receiver
    users.update_one(
        {'account_id': id_receiver},
        {
            '$inc':{'balance': amount},
            '$push':{'transfers_complete': transfer_id}
        },
        session=session
    )

    # edit account sender
    users.update_one(
        {'account_id': id_sender},
        {
            '$inc':{'balance': -amount},
            '$push':{'transfers_complete': transfer_id}
        },
        session=session
    )

    transfers.insert_one(transfer,session=session)
    print("Sucess!")
    return

def callback_wrapper(s):
        callback(
            s,
            transfer_id='TR555',
            id_receiver='MDB574189300',
            id_sender='MDB343652528',
            amount=100,
        )

with client.start_session() as session:
      session.with_transaction(callback_wrapper)
print("Total transfers:", transfers.count_documents({}))

#client.close()