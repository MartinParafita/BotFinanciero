
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
                
    
    elif intervalo == 4:
        intervalo = KLINE_INTERVAL_4HOUR
        data_historical = cliente.get_historical_klines(activo,intervalo,str(horas) + 'hours ago')
        
        if len(data_historical) <= 200:
            for i in range(0, cant_velas):
                sumatoria += float(data_historical[i][4])
                
    
    elif intervalo == 24:
        intervalo = KLINE_INTERVAL_1DAY
        data_historical = cliente.get_historical_klines(activo,intervalo,str(horas) + 'hours ago')
        
        if len(data_historical) <= 200:
            for i in range(0, int(cant_velas)):
                sumatoria += float(data_historical[i][4])
                
        
    sma = (sumatoria / cant_velas)
    print('La media movil simple de ',cant_velas_str ,'periodos es: ',sma)
    return (sma)

def med_movil_exponencial(activo,intervalo,cant_velas):                             #ES UTIL PARA INDICAR CAMBIOS Y CONTINUIDAD DE TENDENCIAS
    
    horas = intervalo * 250
    lista_precios_cierre = []
    ema = []
    
    sma = med_movil_simple(activo,intervalo,cant_velas)
    ema.append(sma)
    
    if intervalo == 1:
        intervalo = KLINE_INTERVAL_1HOUR
        data_historical = cliente.get_historical_klines(activo,intervalo,'250 hours ago UTC')
        
        if len(data_historical) == 250:
            
            for i in range(len(data_historical)):
                lista_precios_cierre.append(float(data_historical[i][4]))
            
            
            for price in lista_precios_cierre[cant_velas:]:
                ema.append((price * (2 / (cant_velas + 1))) + ema[-1] * (1 - (2 /(cant_velas + 1))))
            
            ema_valor = round(ema.pop(),4)
    
    if intervalo == 4:
        intervalo = KLINE_INTERVAL_4HOUR
        data_historical = cliente.get_historical_klines(activo,intervalo,str(horas) +  'hours ago UTC')
        
        if len(data_historical) == 250:
            
            for i in range(len(data_historical)):
                lista_precios_cierre.append(float(data_historical[i][4]))
            
            for price in lista_precios_cierre:
                ema.append((price * (2 / (cant_velas + 1))) + ema[-1] * (1 - (2 /(cant_velas + 1))))
            
            ema_valor = round(ema.pop(),4)

    if intervalo == 24:
        intervalo = KLINE_INTERVAL_1DAY
        data_historical = cliente.get_historical_klines(activo,intervalo,str(horas) +  'hours ago UTC')
        
        if len(data_historical) == 250:
            
            for i in range(len(data_historical)):
                lista_precios_cierre.append(float(data_historical[i][4]))
            
            for price in lista_precios_cierre:
                ema.append((price * (2 / (cant_velas + 1))) + ema[-1] * (1 - (2 /(cant_velas + 1))))
            
            ema_valor = ema.pop
    print('La media movil exponencial de ',cant_velas_str , 'periodos es: ',ema_valor)
    return ema_valor

if __name__ == '__main__':
    print('Bienvenidos al Bot Financiero!\n')

    print('A continuación te presentamos los posibles pares a operar:')
    todos_los_pares()
    lista_de_pares = pd.DataFrame(cliente.get_all_tickers())
    print(lista_de_pares)
    activo = str(input('Que activo desea operar?' ))
    
    print('1. Intervalo de 1 hora')
    print('4. Intervalo de 4 horas')
    print('24. Intervalo de 24 horas')
    intervalo = int(input('Que intervalo horario queres visualizar? '))
    if intervalo != 1 and intervalo != 4 and intervalo != 24:
        print('La opción no existe.')
    
    print('La cantidad maxima de velas es 200')
    cant_velas = int(input('Que cantidad de velas queres visualizar?  '))
    cant_velas_str = str(cant_velas)

    med_movil_simple(activo,intervalo,cant_velas)
    print('----------------------------------------------------')
    med_movil_exponencial(activo,intervalo,cant_velas)
    
    