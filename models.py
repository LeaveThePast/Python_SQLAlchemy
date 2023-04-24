import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    publisher_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    book = relationship('Book', back_populates='publisher')

    def __str__(self):
        return f'publisher_id: {self.publisher_id} | name: {self.name}'


class Book(Base):
    __tablename__ = 'book'
    book_id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey('publisher.publisher_id'), nullable=False)

    publisher = relationship('Publisher', back_populates='book')
    stock = relationship('Stock', back_populates='book')

    def __str__(self):
        return f'book_id: {self.book_id} | title: {self.title} | publisher_id: {self.publisher_id}'


class Shop(Base):
    __tablename__ = 'shop'
    shop_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True, nullable=False)

    stock = relationship('Stock', back_populates='shop')

    def __str__(self):
        return f'shop_id: {self.shop_id} | name: {self.name}'


class Stock(Base):
    __tablename__ = 'stock'
    stock_id = sq.Column(sq.Integer, primary_key=True)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey('shop.shop_id'), nullable=False)
    book_id = sq.Column(sq.Integer, sq.ForeignKey('book.book_id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship('Book', back_populates='stock')
    shop = relationship('Shop', back_populates='stock')
    sale = relationship('Sale', back_populates='stock')

    def __str__(self):
        return f'stock_id: {self.stock_id} | shop_id: {self.shop_id} | book_id: {self.book_id} | count: {self.count}'


class Sale(Base):
    __tablename__ = 'sale'
    sale_id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Double, nullable=False)
    sale_date = sq.Column(sq.DateTime, nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey('stock.stock_id'), nullable=False)

    stock = relationship('Stock', back_populates='sale')

    def __str__(self):
        return f'sale_id: {self.sale_id} | price: {self.price} | sale_date: {self.sale_date} | count: {self.count} | stock_id: {self.stock_id}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
