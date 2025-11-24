import traceback
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from binance.client import Client
import os
from dotenv import load_dotenv
from BotFutures import TradingBot 

app = Flask(__name__)

load_dotenv() # Carga las variables del archivo .env

# --- CONFIGURACIÓN BASE DE DATOS ---
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios_activos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Tus claves 
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Diccionario para guardar los bots en ejecución: 
bots_activos = {}

@app.route("/")
def index():
    # Mostramos los bots que están corriendo actualmente
    return render_template('index.html', activos=bots_activos)

@app.route("/iniciar_bot", methods=['POST'])
def iniciar_bot():
    try:
        # 1. Obtener datos del formulario HTML
        pair = request.form['symbol']       # Ej: BTCUSDT
        interval = request.form['interval'] # Ej: 1d
        cantidad = request.form['cantidad'] # Ej: 0.001

        # 2. Verificar si ya existe un bot para ese par
        if pair in bots_activos:
            return "Ya hay un bot corriendo para este par."

        # 3. Instanciar y arrancar el Bot en un Hilo separado
        nuevo_bot = TradingBot(API_KEY, API_SECRET, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, pair, interval, cantidad)
        nuevo_bot.start() 
        
        # 4. Guardar en el diccionario para controlarlo luego
        bots_activos[pair] = {
            'bot': nuevo_bot,
            'interval': interval
        }
        
        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({'error': traceback.format_exc()})

@app.route("/detener_bot/<symbol>")
def detener_bot(symbol):
    try:
        if symbol in bots_activos:
            
            bot_obj = bots_activos[symbol]['bot']
            bot_obj.detener()
            
            # Lo sacamos de la lista
            bot_obj.join() 
            del bots_activos[symbol]
            
        return redirect(url_for('index'))
    except:
        return "Error deteniendo bot"

# --- CÓDIGO DE CARGA DE PARES  ---

def obtener_pares_usdt():
    try:
        client = Client(API_KEY, API_SECRET) 
        tickers = client.get_ticker()
        lista = [t['symbol'] for t in tickers if "USDT" in t['symbol']]
        return sorted(lista)
    except:
        return []

# Pasamos la lista de pares al contexto de la plantilla siempre
@app.context_processor
def inject_pares():
    return dict(lista_pares=obtener_pares_usdt())

if __name__ == '__main__':
    # Crea las tablas si no existen al iniciar
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)