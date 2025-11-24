from binance.client import Client
from binance.enums import *
import pandas as pd
import time
import requests

# --- CONFIGURACIÓN ---
API_KEY = ''
API_SECRET = ''

# Datos de Telegram
TELEGRAM_TOKEN = ''
TELEGRAM_CHAT_ID = ''

# Configuración de Trading
SYMBOL = 'ETHUSDT'         # El par a operar
CANTIDAD = 0.01           # Cantidad de cripto a operar 
TIMEFRAME = Client.KLINE_INTERVAL_1DAY  # Intervalo de 24hs
TRAILING_PERCENT = 7      # Porcentaje del Trailing Stop (7%)

# Conexión 
client = Client(API_KEY, API_SECRET)

# --- FUNCIONES ---

def enviar_telegram(mensaje):
    """Envía mensajes a tu Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
        requests.post(url, data=data)
    except Exception as e:
        print(f"Error enviando Telegram: {e}")

def obtener_datos(simbolo, intervalo):
    """Descarga velas y calcula medias móviles con Pandas."""
    # Traemos 200 velas para tener datos suficientes para la media de 50
    klines = client.futures_klines(symbol=simbolo, interval=intervalo, limit=200)
    
    # Convertimos a DataFrame de Pandas para cálculos rápidos
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    
    # Limpiamos datos y convertimos a números
    df = df[['timestamp', 'close']]
    df['close'] = pd.to_numeric(df['close'])
    
    # --- CÁLCULO DE MEDIAS MÓVILES (SMA) ---
    # Aquí reemplazamos tu lógica manual. Pandas lo hace automático:
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()
    
    return df

def ejecutar_orden(lado, cantidad, simbolo):
    """Ejecuta la orden de mercado y configura el Trailing Stop."""
    try:
        print(f"--------------------------------")
        print(f"EJECUTANDO OPERACIÓN: {lado}")
        
        # 1. Ejecutar la orden de entrada (MARKET)
        # Si es LONG, compramos. Si es SHORT, vendemos.
        order = client.futures_create_order(
            symbol=simbolo,
            side=lado,
            type='MARKET',
            quantity=cantidad
        )
        precio_entrada = order['avgPrice'] # Precio promedio de entrada
        msg_entrada = f"🚀 Orden {lado} ejecutada en {simbolo} a ${precio_entrada}"
        print(msg_entrada)
        enviar_telegram(msg_entrada)
        
        # 2. Configurar el TRAILING STOP LOSS
        # Si entramos en LONG (BUY), el Stop Loss es una orden de VENTA (SELL).
        # Si entramos en SHORT (SELL), el Stop Loss es una orden de COMPRA (BUY).
        lado_stop = SIDE_SELL if lado == SIDE_BUY else SIDE_BUY
        
        # El callbackRate es el porcentaje que el precio debe retroceder para cerrar.
        # Esto cumple tu requisito: "Si el precio sube, quiero ir subiendo el STOP LOSS".
        stop_order = client.futures_create_order(
            symbol=simbolo,
            side=lado_stop,
            type='TRAILING_STOP_MARKET',
            quantity=cantidad,
            callbackRate=TRAILING_PERCENT # 10% de retroceso
        )
        print(f"🛡️ Trailing Stop del {TRAILING_PERCENT}% configurado exitosamente.")
        enviar_telegram(f"🛡️ Trailing Stop activado al {TRAILING_PERCENT}% de distancia.")
        
    except Exception as e:
        msg_error = f"⚠️ Error ejecutando orden: {e}"
        print(msg_error)
        enviar_telegram(msg_error)

def estrategia():
    print(f"🤖 Bot Iniciado en {SYMBOL} ({TIMEFRAME}). Esperando cruce de medias...")
    enviar_telegram(f"🤖 Bot Iniciado en {SYMBOL}. Buscando cruces SMA 20/50.")
    
    # Bandera simple para no operar dos veces seguidas en la misma dirección
    # En un bot real, deberías consultar client.futures_position_information()
    en_posicion = False 

    while True:
        try:
            df = obtener_datos(SYMBOL, TIMEFRAME)
            
            # Tomamos las dos últimas velas cerradas/actuales
            # iloc[-1] es la vela actual (en formación), iloc[-2] es la vela anterior cerrada
            ultima_vela = df.iloc[-1]
            vela_anterior = df.iloc[-2]
            
            sma20_actual = ultima_vela['sma_20']
            sma50_actual = ultima_vela['sma_50']
            sma20_prev = vela_anterior['sma_20']
            sma50_prev = vela_anterior['sma_50']
            
            precio_actual = ultima_vela['close']
            
            print(f"Precio: {precio_actual} | SMA20: {round(sma20_actual,2)} | SMA50: {round(sma50_actual,2)}")
            
            # Chequeamos si hay cruce solo si no estamos en posición (o si queremos invertir la mano)
            # Nota: Para simplificar, este código asume que el Stop Loss te saca del mercado antes del siguiente cruce.
            
            # --- LÓGICA DE CRUCE AL ALZA (LONG) ---
            # La media rápida (20) cruza hacia ARRIBA a la lenta (50)
            if sma20_prev < sma50_prev and sma20_actual > sma50_actual:
                print("¡CRUCE DORADO DETECTADO! (LONG)")
                ejecutar_orden(SIDE_BUY, CANTIDAD, SYMBOL)
                en_posicion = True
                time.sleep(60 * 60 * 24) # Esperamos un día para no re-operar en la misma vela (simple)
                
            # --- LÓGICA DE CRUCE A LA BAJA (SHORT) ---
            # La media rápida (20) cruza hacia ABAJO a la lenta (50)
            elif sma20_prev > sma50_prev and sma20_actual < sma50_actual:
                print("¡CRUCE DE LA MUERTE DETECTADO! (SHORT)")
                ejecutar_orden(SIDE_SELL, CANTIDAD, SYMBOL)
                en_posicion = True
                time.sleep(60 * 60 * 24) # Esperamos un día

            # Esperamos un tiempo prudencial antes de volver a chequear
            time.sleep(60) 

        except Exception as e:
            print(f"Error en el bucle principal: {e}")
            time.sleep(10)

if __name__ == '__main__':
    estrategia()