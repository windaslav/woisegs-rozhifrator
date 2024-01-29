import telebot
import speech_recognition as sr
from pydub import AudioSegment
import requests
import psutil

bot = telebot.TeleBot("вставьте суда токен от бота")

# Функция для обработки голосовых сообщений
@bot.message_handler(content_types=['voice'])
def voice_to_text(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format("вставьте суда свой токен от бота", file_info.file_path))
    with open('voice.ogg', 'wb') as f:
        f.write(file.content)

    audio = AudioSegment.from_file("voice.ogg", format="ogg")
    audio.export("voice.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        bot.reply_to(message, text)
    except sr.UnknownValueError:
        bot.reply_to(message, "Извините, не удалось распознать голосовое сообщение")
    except sr.RequestError:
        bot.reply_to(message, "Извините, возникла проблема с обработкой вашего запроса")

# Функция для обработки текстовых сообщений
@bot.message_handler(commands=['status'])
def send_status(message):
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    response = f"Загрузка CPU: {cpu_percent}%\n" \
               f"Загрузка памяти: {memory_percent}%\n" \
               f"Загрузка диска: {disk_percent}%"
    bot.reply_to(message, response)

bot.polling()
