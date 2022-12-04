import telebot
from telebot import types
import speech_recognition as sr
import os
import gtts


class Bot:
    MypyBot = telebot.TeleBot('token place', parse_mode = None)
    recognizer = sr.Recognizer()
    self_link = ''

    def __init__(self):
        """Constructor"""
        self.MypyBot.polling()
        self_link = self
        print('\nObject bot created\n')

    @MypyBot.message_handler(commands= ['start'])
    def start(message, bot = MypyBot):       
        bot.send_message(message.chat.id, f'Hi {message.from_user.first_name}, i will try to translate your audio in to text and you text in audio')


    def recognise(filename, r=recognizer, language='ru_RU'):
        with sr.AudioFile(filename) as source:
            audio_text = r.listen(source)
            try:
                text = r.recognize_google(audio_text,language=language)
                print('Converting audio transcripts into text ...')                
                return text
            except Exception:
                print('Sorry.. run again...')
                return Exception

    @MypyBot.message_handler(func=lambda message: True, content_types=['text'])
    def text_recognizer(message, bot = MypyBot, r = recognise):
        bot.send_message(message.chat.id, f"you really want to voice this?\n\n")
        text = gtts.gTTS(message.text, lang='ru')
        text.save("voiced.oga")
        voice = open("voiced.oga", 'rb')
        bot.send_audio(message.chat.id, voice)


    @MypyBot.message_handler(func=lambda message: True, content_types=['audio', 'voice'])
    def handle_docs_document(message, bot = MypyBot, r = recognise):
        bot.send_message(message.chat.id, f"actually i try to work\n\n ok give me your garbage")
        if message.content_type ==  'voice':

            file_info = bot.get_file(message.voice.file_id)
            
            file_name_full = file_info.file_path
            file_name_full_converted = file_info.file_path.replace('.oga','_c.wav')
            
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_name_full, 'wb') as new_file:
                new_file.write(downloaded_file)
            print('\n\n\n created')
            os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
            print('\n\n\n converted')
            text=r(file_name_full_converted)
            bot.reply_to(message, text)
            os.remove(file_name_full)
            os.remove(file_name_full_converted)

            print("ok this voice")
        if message.content_type ==  'audio':
            bot.send_message(message.chat.id, f"I dont work with that.\n Only voice message")
      