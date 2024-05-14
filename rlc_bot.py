from telegram.ext import Updater, CommandHandler, CallbackContext
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Función para obtener las novedades de la página de lanzamientos de Hotwheels RLC
def obtener_novedades():
    url = "https://creations.mattel.com/pages/launch-calendar"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    novedades = soup.find("div", class_="launch-calendar").find_all("div", class_="col-lg-6")
    return [novedad.text.strip() for novedad in novedades]

# Función para verificar si hay un modelo RLC que se lanza hoy
def verificar_lanzamiento_hoy():
    hoy = datetime.now().strftime("%A, %B %d, %Y")
    novedades = obtener_novedades()
    for novedad in novedades:
        if hoy in novedad:
            return True
    return False

# Función para obtener el modelo RLC que se ha lanzado hoy
def obtener_modelo_lanzado_hoy():
    hoy = datetime.now().strftime("%A, %B %d, %Y")
    novedades = obtener_novedades()
    for novedad in novedades:
        if hoy in novedad:
            nombre_modelo = novedad.split("\n")[0]
            return nombre_modelo
    return None

# Función para enviar un mensaje al grupo cuando hay nuevas novedades
def enviar_novedades(update, context):
    novedades = obtener_novedades()
    for novedad in novedades:
        context.bot.send_message(chat_id=update.effective_chat.id, text=novedad)

# Función para enviar un mensaje al grupo el día del lanzamiento de un modelo RLC
def enviar_aviso_lanzamiento(context: CallbackContext):
    if verificar_lanzamiento_hoy():
        nombre_modelo = obtener_modelo_lanzado_hoy()
        if nombre_modelo:
            mensaje = f"¡Hoy sale un nuevo modelo Hotwheels RLC! 🚗💨\n\n"
            mensaje += f"Nombre del modelo: {nombre_modelo}"
            context.bot.send_message(chat_id=CHAT_ID, text=mensaje)

# Configuración del bot
TOKEN = "7175013590:AAEJVSIawUsewRPGhoLyqetaV8cPAfxh7qg"  # Reemplaza "TU_TOKEN_AQUÍ" con el token de tu bot
CHAT_ID = "4265548733"  # Reemplaza "TU_CHAT_ID_AQUÍ" con el ID del grupo donde quieres enviar los mensajes

# Crear un objeto Updater y pasarle el token del bot
updater = Updater(token=TOKEN, use_context=True)

# Obtener el despachador para registrar los manejadores
dispatcher = updater.dispatcher

# Registrar un manejador para el comando /start
dispatcher.add_handler(CommandHandler("start", enviar_novedades))

# Iniciar el bot
updater.start_polling()

# Programar el envío de avisos de lanzamiento cada día a las 8:00 AM
updater.job_queue.run_daily(enviar_aviso_lanzamiento, time=datetime.time(hour=8))

# Mantener el bot ejecutándose
updater.idle()
