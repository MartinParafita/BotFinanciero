from binance.client import Client
from binance.enums import *
import pandas as pd
import pandas_ta as ta  
import time


# --- CONFIGURACIÓN ---
API_KEY = '9NAOJLUjwp7JC24F0YehqNrNXkZcTZYuBhcjkJpUCooKDsLRTKhCS2jqlzRLbkk7'
API_SECRET = 'y6uUJp2XfuhOAS4RSzVDw2umutMlIzeMThJ1X6VsTS9dIHqcjHTiWte7JqMELx5w'
SYMBOL = 'ETHUSDT'
CANTIDAD = 0.01             
TIMEFRAME = Client.KLINE_INTERVAL_1DAY 
TRAILING_PERCENT = 7.0     # Porcentaje del trailing
ADX_UMBRAL = 25            # El filtro de fuerza de tendencia

client = Client(API_KEY, API_SECRET, tld="com")

def obtener_datos(simbolo, intervalo):
    
    klines = client.futures_klines(symbol=simbolo, interval=intervalo, limit=150)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    
    # Convertir a numérico
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    
    # --- CÁLCULO DE INDICADORES CON PANDAS-TA ---
    
    # 1. Medias Móviles
    df['sma_20'] = ta.sma(df['close'], length=20)
    df['sma_50'] = ta.sma(df['close'], length=50)
    
    # 2. ADX (Retorna un DataFrame con ADX_14, DMP_14, DMN_14)
    # Usamos length=14 que es el estándar que tienes en tu gráfico
    adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
    
    # Unimos el resultado del ADX al DataFrame principal
    # La columna se suele llamar 'ADX_14' por defecto en la librería
    df = pd.concat([df, adx_df], axis=1)
    
    return df

def check_posicion_abierta(simbolo):
    try:
        info = client.futures_position_information(symbol=simbolo)
        for i in info:
            if i['symbol'] == simbolo:
                amt = float(i['positionAmt'])
                if amt != 0:
                    return True
        return False
    except Exception as e:
        print(f"Error api: {e}")
        return True 

def ejecutar_orden(lado, cantidad, simbolo):
    try:
        print(f"🚀 EJECUTANDO ENTRADA: {lado}")
        client.futures_create_order(symbol=simbolo, side=lado, type='MARKET', quantity=cantidad)
        
        lado_stop = SIDE_SELL if lado == SIDE_BUY else SIDE_BUY
        client.futures_create_order(
            symbol=simbolo, 
            side=lado_stop, 
            type='TRAILING_STOP_MARKET', 
            quantity=cantidad, 
            callbackRate=TRAILING_PERCENT
        )
        print("✅ Orden y Trailing Stop configurados.")
    except Exception as e:
        print(f"❌ Error ejecutando orden: {e}")

def estrategia():
    print(f"--- BOT INICIADO: {SYMBOL} (1D) | ADX > {ADX_UMBRAL} ---")
    
    while True:
        try:
            if check_posicion_abierta(SYMBOL):
                print("Posición abierta. Esperando cierre...")
                time.sleep(60) 
                continue

            df = obtener_datos(SYMBOL, TIMEFRAME)
            actual = df.iloc[-1]
            previo = df.iloc[-2]
            
            # Variables para legibilidad
            sma20_hoy = actual['sma_20']
            sma50_hoy = actual['sma_50']
            sma20_ayer = previo['sma_20']
            sma50_ayer = previo['sma_50']
            
            # Obtenemos el valor del ADX actual. 
            # Nota: A veces la columna se llama 'ADX_14', verifica imprimiendo df.columns si falla
            adx_actual = actual['ADX_14'] 
            
            print(f"Precio: {actual['close']} | SMA20: {round(sma20_hoy,1)} | SMA50: {round(sma50_hoy,1)} | ADX: {round(adx_actual, 1)}")

            # --- LÓGICA DE TRADING ---
            
            # 1. Definimos si hubo cruce
            cruce_alcista = sma20_ayer < sma50_ayer and sma20_hoy > sma50_hoy
            cruce_bajista = sma20_ayer > sma50_ayer and sma20_hoy < sma50_hoy
            
            # 2. Definimos si hay fuerza (Filtro ADX)
            hay_fuerza = adx_actual > ADX_UMBRAL

            if cruce_alcista:
                if hay_fuerza:
                    print("📈 CRUCE ALCISTA + FUERZA CONFIRMADA -> GO LONG")
                    ejecutar_orden(SIDE_BUY, CANTIDAD, SYMBOL)
                else:
                    print("⚠️ Cruce Alcista ignorado (ADX muy bajo, mercado lateral)")
                    
            elif cruce_bajista:
                if hay_fuerza:
                    print("📉 CRUCE BAJISTA + FUERZA CONFIRMADA -> GO SHORT")
                    ejecutar_orden(SIDE_SELL, CANTIDAD, SYMBOL)
                else:
                    print("⚠️ Cruce Bajista ignorado (ADX muy bajo, mercado lateral)")
            
            time.sleep(60) 

        except Exception as e:
            print(f"Error bucle: {e}")
            time.sleep(10)

if __name__ == '__main__':
    estrategia()