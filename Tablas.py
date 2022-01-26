


from flask import session
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from binance.client import Client
from binance.enums import *
API_KEY = 'cidV4hzfstUlcvQh5v7ciaA7vSmmaWdHzfomQhESZJRiLqsN5PKEKmADgsgkPUEK'        #NOMBRE DE LA API DE BINANCE
API_SECRET = 'Ddju4c7rg8U9GfypjTXrl9fSvOrXo0c0LXLZfp6yne2FZ2HiWc0brjIWOEd75RUH'
cliente = Client(API_KEY,API_SECRET, tld = 'com')  


engine = sqlalchemy.create_engine("sqlite:///usuarios_activos.db")
base = declarative_base()

class Usuarios(base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)

    def __repr__(self):
        return f"Su numero de usuario es: {self.id}"

class Activos(base):
    __tablename__ = 'activos'
    par = Column(String, primary_key=True)
    precio_actual = Column(Float)
    
    def __repr__(self):
        return f'El activo', {self.par}, 'se agrego correctamente.'

class Datos(base):
    __tablename__ = 'prueba'
    symbol = Column(String, primary_key=True)
    priceChange = Column(Float)
    priceChangePercent = Column(Float)
    prevClosePrice = Column(Float)
    lastPrice = Column(Float)
    openPrice = Column(Float)
    highPrice = Column(Float)
    lowPrice = Column(Float)
    volume = Column(Float)
    openTime = Column(Integer)
    closeTime = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return self.symbol

def crear_tablas():
    
    base.metadata.create_all(engine)

def insert_usuario(nombre, apellido):
    
    Session = sessionmaker(bind=engine)
    session = Session()
    person = Usuarios(nombre=nombre, apellido=apellido)
    session.add(person)
    session.commit()
    print(person)

def insert_pares():
    pares = cliente.get_all_tickers()
    Session = sessionmaker(bind=engine)
    session = Session()
    for par in pares:
        dict= par
        symbol = dict['symbol']
        price = float(dict['price'])
        prueba = Activos(par=symbol, precio_actual=price)
        session.add(prueba)
        session.commit()
    
def insert_datos():
    data = cliente.get_ticker()
    Session = sessionmaker(bind=engine)
    session = Session()
    for i in data:
        d = i
        symbol = d['symbol']
        priceChange = float(d['priceChange'])
        priceChangePercent = float(d['priceChangePercent'])
        prevClosePrice = float(d['prevClosePrice'])
        lastPrice = float(d['lastPrice'])
        openPrice = float(d['openPrice'])
        highPrice = float(d['highPrice'])
        lowPrice = float(d['lowPrice'])
        volume = float(d['volume'])
        openTime = int(d['openTime'])
        closeTime = int(d['closeTime'])
        count = int(d['count'])
        info = Datos(symbol=symbol, priceChange=priceChange,priceChangePercent=priceChangePercent,prevClosePrice=prevClosePrice,lastPrice=lastPrice,openPrice=openPrice,highPrice=highPrice,lowPrice=lowPrice,volume=volume,openTime=openTime,closeTime=closeTime,count=count)
        session.add(info)
        session.commit()


if __name__ == '__main__':
    crear_tablas()
    insert_usuario('Martin','Parafita')
    insert_pares()
    insert_datos()
    