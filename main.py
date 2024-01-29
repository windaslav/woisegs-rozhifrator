import telebot
import speech_recognition as sr
from pydub import AudioSegment
import requests

bot = telebot.TeleBot("вставьте суда свой токен")

# Функция для обработки голосовых сообщений
@bot.message_handler(content_types=['voice'])
def voice_to_text(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format("в ведите суда свой токен от бота", file_info.file_path))
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
        bot.reply_to(message, "Извините, не удалось распознать голосовое сообщение, идите нахер, или попробуйте ещё раз")
    except sr.RequestError:
        bot.reply_to(message, "Извините, возникла проблема с обработкой вашего запроса")

bot.polling()
