
from flask_sqlalchemy import SQLAlchemy
from binance.client import Client
from binance.enums import *


API_KEY = 'cidV4hzfstUlcvQh5v7ciaA7vSmmaWdHzfomQhESZJRiLqsN5PKEKmADgsgkPUEK'        #NOMBRE DE LA API DE BINANCE
API_SECRET = 'Ddju4c7rg8U9GfypjTXrl9fSvOrXo0c0LXLZfp6yne2FZ2HiWc0brjIWOEd75RUH'
cliente = Client(API_KEY,API_SECRET, tld = 'com')  

db = SQLAlchemy()


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String)
    apellido = db.Column(db.String)

    def __repr__(self):
        return f"Su numero de usuario es: {self.id}"


class Datos(db.Model):
    __tablename__ = 'prueba'
    symbol = db.Column(db.String, primary_key=True)
    priceChange = db.Column(db.Float)
    priceChangePercent = db.Column(db.Float)
    prevClosePrice = db.Column(db.Float)
    lastPrice = db.Column(db.Float)
    openPrice = db.Column(db.Float)
    highPrice = db.Column(db.Float)
    lowPrice = db.Column(db.Float)
    volume = db.Column(db.Float)
    openTime = db.Column(db.Integer)
    closeTime = db.Column(db.Integer)
    count = db.Column(db.Integer)

    def __repr__(self):
        return self.symbol


def insert_usuario(nombre, apellido):
    if (nombre,apellido) is not Usuarios:
        person = Usuarios(nombre=nombre, apellido=apellido)
        db.session.add(person)
        db.session.commit()
    else:
        print('El usuario ya existe')
    
    
def insert_datos():
    data = cliente.get_ticker()
    lista_USDT = []
    for i in data:
        if "USDT" in i['symbol']:
            lista_USDT.append(i)
    for i in lista_USDT:
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
        db.session.add(info)
        db.session.commit()
    return d



if __name__ == '__main__':
    
    insert_usuario('Martin','Parafita')
    insert_datos()
    