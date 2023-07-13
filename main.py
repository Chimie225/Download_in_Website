import os
import subprocess
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler


# Fonction pour télécharger la vidéo à partir du lien
def download_video(url):
    file_name = 'video.mp4'
    command = ['youtube-dl', '-o', file_name, url]
    subprocess.call(command)
    return file_name

# Fonction pour gérer les messages
def handle_message(update, context):
    message = update.message
    if message.text.startswith('http'):
        video_url = message.text
        video_file = download_video(video_url)
        chat_id = message.chat_id
        caption = 'Développé par @elisa2w'
        context.bot.send_video(chat_id=chat_id, video=open(video_file, 'rb'), caption=caption)
        os.remove(video_file)  # Supprimer le fichier après l'envoi

# Fonction pour gérer le message de bienvenue
def handle_start(update, context):
    message = update.message
    chat_id = message.chat_id
    welcome_message = 'Bonjour ! Je suis un bot de téléchargement de vidéos. Envoyez-moi un lien vidéo pour le télécharger.'
    context.bot.send_message(chat_id=chat_id, text=welcome_message)

# Créer un dossier pour les fichiers téléchargés
download_folder = '/sdcard/Lien'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Initialiser le bot Telegram
bot_token = '6389963856:AAG4_cX7znFhn9k0m-INc-XYmX1zy-43FiE'
updater = Updater(bot_token)

# Ajouter un gestionnaire de messages au bot
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.dispatcher.add_handler(CommandHandler('start', handle_start))

# Démarrer le bot
updater.start_polling()
updater.idle()
