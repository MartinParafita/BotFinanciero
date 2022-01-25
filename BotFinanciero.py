
from binance.client import Client
from binance.enums import *
import sqlalchemy
import pandas as pd
import Tablas

API_KEY = 'cidV4hzfstUlcvQh5v7ciaA7vSmmaWdHzfomQhESZJRiLqsN5PKEKmADgsgkPUEK'        #NOMBRE DE LA API DE BINANCE
API_SECRET = 'Ddju4c7rg8U9GfypjTXrl9fSvOrXo0c0LXLZfp6yne2FZ2HiWc0brjIWOEd75RUH'     #CONTRASEÑA DE LA API DE BINANCE

cliente = Client(API_KEY,API_SECRET, tld = 'com')                                   #NOS CONECTAMOS CON LA API DE BINANCE

def todos_los_pares():                                                              #PRESENTAMOS TODOS LOS PARES DISPONIBLES
    lista_de_pares = pd.DataFrame(cliente.get_all_tickers())
    return lista_de_pares

def med_movil_simple(activo,intervalo,cant_velas):                                  #ES UN INDICADOR DEL PRECIO MEDIO DEL ACTIVO EN UN PERIODO DETERMINADO
    

    sumatoria = 0
    horas = intervalo * cant_velas

    if intervalo == 1:
        intervalo = KLINE_INTERVAL_1HOUR
        data_historical = cliente.get_historical_klines(activo,intervalo,str(cant_velas) + 'hours ago')
        
        if len(data_historical) <= 200:
            for i in range(0, int(cant_velas)):
                sumatoria += float(data_historical[i][4])
                print(data_historical[i])
    
    elif intervalo == 4:
        intervalo = KLINE_INTERVAL_4HOUR
        data_historical = cliente.get_historical_klines(activo,intervalo,str(horas) + 'hours ago')
        
        if len(data_historical) <= 200:
            for i in range(0, cant_velas):
                sumatoria += float(data_historical[i][4])
                print(data_historical[i])
    
    elif intervalo == 12:
        intervalo = KLINE_INTERVAL_12HOUR
        data_historical = cliente.get_historical_klines(activo,intervalo,str(horas) + 'hours ago')
        
        if len(data_historical) <= 200:
            for i in range(0, int(cant_velas)):
                sumatoria += float(data_historical[i][4])
                print(data_historical[i])
        
    sma = (sumatoria / cant_velas)
    return print('La media movil simple de ' + cant_velas_str + ' periodos es: ',sma,)

def ultimas_24hs():
    data_24hs = pd.DataFrame(cliente.get_ticker())
    print(data_24hs)

if __name__ == '__main__':
    print('Bienvenidos al Bot Financiero!\n')

    print('A continuación te presentamos los posibles pares a operar:')
    todos_los_pares()
    lista_de_pares = pd.DataFrame(cliente.get_all_tickers())
    print(lista_de_pares)
    activo = str(input('Que activo desea operar?' ))
    
    print('1. Intervalo de 1 hora')
    print('4. Intervalo de 4 horas')
    print('12. Intervalo de 12 horas')
    intervalo = int(input('Que intervalo horario queres visualizar? '))
    if intervalo != 1 and intervalo != 4 and intervalo != 12:
        print('La opción no existe.')
    
    print('La cantidad maxima de velas es 200')
    cant_velas = int(input('Que cantidad de velas queres visualizar?  '))
    cant_velas_str = str(cant_velas)

    med_movil_simple(activo,intervalo,cant_velas)
    print('----------------------------------------------------')
    ultimas_24hs()
    # MODIFICAR LA TABLA DE ACTIVOS PARA QUE MUESTREN TODOS LOS DATOS, ASI PODER HACER EL ANALISIS DE LAS ESTRATEGIAS.
    # HACER UN FILL() CSV,WRITER PARA LLENAR UNA BASE DE DATOS Y PODER ANALIZAR QUE ACTIVOS CUMPLEN CON EL PATRON Y CUALES NO.