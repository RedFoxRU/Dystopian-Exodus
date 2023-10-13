from peewee import *
from config import PWD

db = SqliteDatabase(f'{PWD}/db.db')


class User(Model):
    id = PrimaryKeyField()
    tgid = IntegerField(null=False,unique=True)
    username = CharField(max_length=50)
    balance = IntegerField(default=0)
    rating = IntegerField(default=10)
    
    
    
    class Meta:
        database = db
        
        
def createDatabase():
    pass
    # User.create_table()