import telebot
import subprocess
import speech_recognition as sr
from pydub import AudioSegment

bot = telebot.TeleBot("вставьте суда свой токен")

# Функция для обработки голосовых сообщений
@bot.message_handler(content_types=['voice'])
def voice_to_text(message):
    voice_file_info = bot.get_file(message.voice.file_id)
    voice_file = bot.download_file(voice_file_info.file_path)
    with open('voice.ogg', 'wb') as file:
        file.write(voice_file)

    # Конвертация файла в WAV с помощью pydub
    audio = AudioSegment.from_file("voice.ogg", format="ogg")
    audio.export("voice.wav", format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")
        bot.send_message(message.chat.id, text)
    except sr.UnknownValueError:
        bot.send_message(message.chat.id, "Извините, не удалось распознать голосовое сообщение")
    except sr.RequestError:
        bot.send_message(message.chat.id, "Извините, возникла проблема с обработкой вашего запроса")

bot.polling()