🇪🇸 Versión en Español
Descripción del Proyecto
Este es un bot de trading automatizado, programado en Python, diseñado para ejecutar operaciones de compra y venta en el mercado de Binance Futures basándose en una estrategia de análisis técnico de Medias Móviles (SMA). El bot utiliza un filtro de tendencia (ADX) y notifica todas las acciones y señales a través de Telegram.

1. Requisitos Indispensables (Configuración de Credenciales)
Para que el bot pueda leer datos del mercado, ejecutar órdenes y enviar alertas, es obligatorio configurar las siguientes credenciales personales en el código fuente:

    API KEY y SECRET KEY de Binance:
    
    Propósito: Conexión y ejecución de órdenes en Binance Futures.
    
    Permisos requeridos: "Enable Reading" y "Enable Futures". Si deseas operar, debes aplicar la restricción de IP para habilitar los permisos de trading.
    
    TELEGRAM TOKEN: Identificador del bot de alertas creado con @BotFather.
    
    TELEGRAM CHAT ID: El identificador numérico de tu chat personal para recibir notificaciones.

2. Funcionamiento de la Aplicación (Estrategia)
La lógica del bot se basa en una estrategia de seguimiento de tendencia que combina el cruce de medias móviles con un filtro de fuerza:

    Indicadores Utilizados
    Media Móvil Rápida (SMA 20): Línea de señal.
    
    Media Móvil Lenta (SMA 50): Línea base de tendencia.
    
    Filtro ADX (Average Directional Index): Mide la fuerza de la tendencia.
    
    Señales de Trading
    Cruce Dorado (Señal de Compra / LONG):
    
    Condición 1: La SMA 20 cruza por encima de la SMA 50.
    
    Condición 2 (Filtro): El valor del ADX es mayor a 25, lo que confirma que hay una tendencia fuerte antes de abrir la posición.
    
    Acción: Se ejecuta una orden de compra (SIDE_BUY).
    
    Cruce de la Muerte (Señal de Venta / SHORT):
    
    Condición 1: La SMA 20 cruza por debajo de la SMA 50.
    
    Condición 2 (Filtro): El valor del ADX es mayor a 25.
    
    Acción: Se ejecuta una orden de venta (SIDE_SELL).
    
    Gestión de Posición y Riesgo
    Trailing Stop: El bot aplica un Trailing Stop configurable al 7.0% (TRAILING_PERCENT = 7.0) para proteger las ganancias si el precio se revierte.
    
    Control Temporal: Una vez que se abre una posición, el bot entra en un estado de espera de 24 horas para evitar re-operar en la misma vela o cruce y darle tiempo al mercado para     desarrollarse.
    
    Alertas: Cada acción relevante (detección de señal, apertura de posición, gestión de cierre) se notifica inmediatamente vía Telegram.

######################################################################################################
######################################################################################################
######################################################################################################

🇺🇸 English Version
Project Description
This is an automated trading bot, programmed in Python, designed to execute buy and sell operations in the Binance Futures market based on a Moving Average (SMA) technical analysis strategy. The bot utilizes a trend filter (ADX) and notifies all actions and signals via Telegram.

1. Essential Requirements (Credentials Setup)
For the bot to successfully read market data, execute orders, and send alerts, it is mandatory to configure the following personal credentials in the source code file:

    Binance API KEY and SECRET KEY:
    
    Purpose: Connection and order execution on Binance Futures.
    
    Required Permissions: "Enable Reading" and "Enable Futures". If you wish to trade, you must apply the IP restriction filter to enable trading permissions.
    
    TELEGRAM TOKEN: Identifier for the Telegram alert bot created with @BotFather.
    
    TELEGRAM CHAT ID: The numerical identifier of your personal chat to receive notifications.

2. Application Functionality (Strategy)
The bot's logic is based on a high-probability trend-following strategy that combines moving average crosses with a strength filter:

    Indicators Used
    Fast Moving Average (SMA 20): Used as the signal line.
    
    Slow Moving Average (SMA 50): Used as the baseline trend line.
    
    ADX Filter (Average Directional Index): Measures the strength of the trend.
    
    Trading Signals
    Golden Cross (Buy Signal / LONG):
    
    Condition 1: The SMA 20 crosses above the SMA 50.
    
    Condition 2 (Filter): The ADX value is greater than 25, which confirms a strong and defined trend before opening a position.
    
    Action: A buy order (SIDE_BUY) is executed.
    
    Death Cross (Sell Signal / SHORT):
    
    Condition 1: The SMA 20 crosses below the SMA 50.
    
    Condition 2 (Filter): The ADX value is greater than 25.
    
    Action: A sell order (SIDE_SELL) is executed.
    
    Position and Risk Management
    Trailing Stop: The bot applies a configurable Trailing Stop set at 7.0% (TRAILING_PERCENT = 7.0) to secure profits if the price reverses.
    
    Time Control: Once a position is opened, the bot enters a waiting state of 24 hours to prevent re-trading on the same candle or cross and allow the market time to develop.
    
    Alerts: Every relevant action (signal detection, position opening, closing management) is notified instantly via Telegram.
