
import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect
from flask_sqlalchemy import SQLAlchemy
from BotFinanciero import med_movil_simple
from BotFinanciero import med_movil_exponencial
from BotFinanciero import pares
from binance.client import Client
from binance.enums import *
import sqlalchemy
import pandas as pd



app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuarios_activos.db"
db.init_app(app)

@app.route("/")
def index():
    try:
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/registro", methods=['GET', 'POST'])
def registro():
    try:
        return render_template('registro.html')
    except:
        return 'No pudieron cargarse los datos.'

@app.route("/pares")
def pares():
    try:
        return render_template('pares.html')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route("/estrategias")
def estrategia():
    try:
        med_movil_simple(activo='symbol',intervalo='intervalo',cant_velas='cant_velas')
    except:
        return jsonify({'trace': traceback.format_exc()})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)