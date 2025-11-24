import time
import pandas as pd
import pandas_ta as ta
from binance.client import Client
from binance.enums import *
import threading
import requests

class TradingBot(threading.Thread):
    def __init__(self, api_key, api_secret, symbol, interval, cantidad, tg_token, tg_chat_id):
        threading.Thread.__init__(self)
        self.running = False
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbol = symbol
        self.interval = interval
        self.cantidad = float(cantidad)
        
        self.telegram_token = tg_token      
        self.telegram_chat_id = tg_chat_id  
        
        # Configuración
        self.base_url = 'https://fapi.binance.com'
        self.trailing_percent = 7.0
        self.adx_umbral = 25
        
        # Cliente
        self.client = Client(self.api_key, self.api_secret, base_url=self.base_url)

    # --- NUEVA FUNCIÓN ---
    def enviar_telegram(self, mensaje):
        """Envía mensajes a tu Telegram."""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {"chat_id": self.telegram_chat_id, "text": mensaje}
            requests.post(url, data=data)
        except Exception as e:
            print(f"Error enviando Telegram: {e}")

    def obtener_datos(self):
        klines = self.client.futures_klines(symbol=self.symbol, interval=self.interval, limit=150)
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        
        # Indicadores
        df['sma_20'] = ta.sma(df['close'], length=20)
        df['sma_50'] = ta.sma(df['close'], length=50)
        adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
        df = pd.concat([df, adx_df], axis=1)
        return df

    def ejecutar_orden(self, lado):
        """Ejecuta la orden de mercado y configura el Trailing Stop."""
        try:
            print(f"--------------------------------")
            print(f"EJECUTANDO OPERACIÓN: {lado}")
            
            # 1. Ejecutar la orden de entrada (MARKET)
            order = self.client.futures_create_order(
                symbol=self.symbol,
                side=lado,
                type='MARKET',
                quantity=self.cantidad
            )
            precio_entrada = order.get('avgPrice', 'N/A') 
            msg_entrada = f" Bot {self.symbol}: {lado} ejecutada a ${precio_entrada}"
            print(msg_entrada)
            self.enviar_telegram(msg_entrada) # AVISO TELEGRAM

            # 2. Configurar el TRAILING STOP LOSS
            lado_stop = SIDE_SELL if lado == SIDE_BUY else SIDE_BUY
            
            stop_order = self.client.futures_create_order(
                symbol=self.symbol, side=lado_stop, type='TRAILING_STOP_MARKET', 
                quantity=self.cantidad, callbackRate=self.trailing_percent
            )
            msg_stop = f" Bot {self.symbol}: Trailing Stop ({self.trailing_percent}%) activado."
            print(msg_stop)
            self.enviar_telegram(msg_stop) # AVISO TELEGRAM
            
        except Exception as e:
            msg_error = f" Error en {self.symbol} ejecutando orden: {e}"
            print(msg_error)
            self.enviar_telegram(msg_error) # AVISO TELEGRAM DE ERROR

    def run(self):
        """Esta función se ejecuta cuando llamamos a bot.start()"""
        self.running = True
        print(f"--- BOT INICIADO PARA {self.symbol} ---")
        
        while self.running:
            try:
                df = self.obtener_datos()
                actual = df.iloc[-1]
                previo = df.iloc[-2]
                
                sma20_hoy = actual['sma_20']
                sma50_hoy = actual['sma_50']
                sma20_ayer = previo['sma_20']
                sma50_ayer = previo['sma_50']
                adx = actual['ADX_14']

                # Lógica simplificada para el ejemplo
                cruce_alcista = sma20_ayer < sma50_ayer and sma20_hoy > sma50_hoy
                cruce_bajista = sma20_ayer > sma50_ayer and sma20_hoy < sma50_hoy
                
                print(f"{self.symbol}: Precio {actual['close']} | ADX {round(adx,2)}")

                if adx > self.adx_umbral:
                    if cruce_alcista:
                        self.ejecutar_orden(SIDE_BUY)
                    elif cruce_bajista:
                        self.ejecutar_orden(SIDE_SELL)
                
                time.sleep(10) # Chequeo cada 10 segs para probar (en prod pon 60)
                
            except Exception as e:
                print(f"Error en bucle: {e}")
                time.sleep(5)

    def detener(self):
        self.running = False
        print("--- DETENIENDO BOT... ---")