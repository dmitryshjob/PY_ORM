import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models_ORM import create_tables,Publisher, Sale, Book, Stock, Shop
import pandas as pd

DSN = "postgresql://postgres:Az1111@localhost:5432/orm"

engine = sqlalchemy.create_engine(DSN) # движок
create_tables(engine)

Session = sessionmaker(bind = engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


request = str(input('Введите имя  :'))



for x in session.query(Book).join(Publisher).filter(Publisher.name == request):
    print(x)


for y in session.query(Shop).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == request):    
    print(y)

for z in session.query(Sale).join(Stock.book).join(Book.publisher).filter(Publisher.name == request):
    print(z)


session.commit()

session.close()