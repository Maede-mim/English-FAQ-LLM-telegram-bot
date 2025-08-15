from tinydb import TinyDB
from tinydb.table import Document


class DBHandler:
    def __init__(self, db_path='F:/Pytopia/FAQ LLM Telegram Bot/messages_db.json'):
        self.db = TinyDB(db_path)
        self.message = self.db.table('message')

    def store_message(self , json_data):
        message_id = json_data.get('message_id')
        if message_id:
            self.message.upsert(Document(json_data,doc_id = message_id))
        else :
            self.message.insert(json_data)

    def  get_message(self,message_id):
        return self.message.get(doc_id=message_id)
    

    def delete_message(self , message_id):
        self.message.remove(doc_ids=[message_id])

    def get_all_message(self):
        return self.message.all()
    
    def close(self):
        self.db.close()