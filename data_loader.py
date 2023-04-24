import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale
import json


DSN = 'postgresql://postgres:6996@localhost:5432/SQLAlchemy'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def load_data(data_file):
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for data_element in data:
            if data_element['model'] == 'publisher':
                current = Publisher(publisher_id=data_element['pk'], name=data_element['fields']['name'])
                session.add(current)
            elif data_element['model'] == 'book':
                current = Book(book_id=data_element['pk'], title=data_element['fields']['title'],
                               publisher_id=data_element['fields']['id_publisher'])
                session.add(current)
            elif data_element['model'] == 'shop':
                current = Shop(shop_id=data_element['pk'], name=data_element['fields']['name'])
                session.add(current)
            elif data_element['model'] == 'stock':
                current = Stock(stock_id=data_element['pk'], shop_id=data_element['fields']['id_shop'],
                                book_id=data_element['fields']['id_book'], count=data_element['fields']['count'])
                session.add(current)
            elif data_element['model'] == 'sale':
                current = Sale(sale_id=data_element['pk'], price=data_element['fields']['price'],
                               sale_date=data_element['fields']['date_sale'], count=data_element['fields']['count'],
                               stock_id=data_element['fields']['id_stock'])
                session.add(current)
            else:
                print('Неопределенный тип данных')
            session.commit()