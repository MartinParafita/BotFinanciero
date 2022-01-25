
from itertools import count
from symtable import Symbol
from flask import session
import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey, column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



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

class Prueba(base):
    __tablename__ = 'prueba'
    symbol = Column(String, primary_key=True)
    priceChange = Column(Float)
    priceChangePercent = Column(Float)
    weightedAvgPrice = Column(Float)
    PrevClosePrice = Column(Float)
    lastPrice = Column(Float)
    lastQty = Column(Float)
    bidPrice = Column(Float)
    bidQty = Column(Float)
    askPrice = Column(Float)
    askQty = Column(Float)
    openPrice = Column(Float)
    highPrice = Column(Float)
    lowPrice = Column(Float)
    volume = Column(Float)
    quoteVolume = Column(Float)
    openTime = Column(Integer)
    closeTime = Column(Integer)
    firstId = Column(Integer)
    lastId = Column(Integer)
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

def insertar_activo(symbol, priceChange, priceChangePercent, weightedAvgPrice, PrevClosePrice, 
    lastPrice,
    lastQty,
    bidPrice,
    bidQty,
    askPrice,
    askQty,
    openPrice,
    highPrice,
    lowPrice,
    volume,
    quoteVolume,
    openTime,
    closeTime,
    firstId,
    lastId,
    count):
    Session = sessionmaker(bind=engine)
    session = Session()
    activo = Prueba(symbol=symbol, priceChange=priceChange, priceChangePercent=priceChangePercent, weightedAvgPrice=weightedAvgPrice, PrevClosePrice=PrevClosePrice, 
    lastPrice=lastPrice,
    lastQty=lastQty,
    bidPrice=bidPrice,
    bidQty=bidQty,
    askPrice=askPrice,
    askQty=askQty,
    openPrice=openPrice,
    highPrice=highPrice,
    lowPrice=lowPrice,
    volume=volume,
    quoteVolume=quoteVolume,
    openTime=openTime,
    closeTime=closeTime,
    firstId=firstId,
    lastId=lastId,
    count=count)
    session.add(activo)
    session.commit()
    print(activo)



if __name__ == '__main__':
    crear_tablas()
    insert_usuario('Martin','Parafita')
    insertar_activo()