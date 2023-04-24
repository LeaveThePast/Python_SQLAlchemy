import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from data_loader import load_data


DSN = 'postgresql://postgres:6996@localhost:5432/SQLAlchemy'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)
load_data('test_data.json')

Session = sessionmaker(bind=engine)
session = Session()

publisher = input('Введите идентификатор издателя: ')


subq1 = session.query(Book).join(Publisher.book).subquery('subq1')

subq2 = session.query(
    Stock,
    subq1.c.title.label('book_title'),
    subq1.c.publisher_id.label('publisher_id'),
    Shop.name.label('shop_name')
).join(subq1, Stock.book_id == subq1.c.book_id).\
join(Shop, Stock.shop_id == Shop.shop_id).subquery('subq2')

q = session.query(
    Sale,
    subq2.c.shop_name,
    subq2.c.book_title
).join(subq2, Sale.stock_id == subq2.c.stock_id).\
    filter(subq2.c.publisher_id == publisher).all()

for sale, shop_name, book_title in q:
    print(f'Sale ID: {sale.sale_id} | Price: {sale.price} | Sale date: {sale.sale_date} | Count: {sale.count} | Shop Name: {shop_name} | Book Title: {book_title}')