#create chat GPT telegramm bot from python  

import os
import openai
from dotenv import load_dotenv
import telebot

load_dotenv()
prompt = ''
user_context = {}
bot = telebot.TeleBot(os.getenv('TELEGRAM_API_KEY'))
openai.api_key = os.getenv('OPENAI_API_KEY')
    
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я чатбот основанный на OpenAI. Спроси меня что нибудь или напиши команду /help.")

@bot.message_handler(commands=['clm'])
def clm(message):
    global user_context
    chat_id = message.chat.id
    if chat_id in user_context:
            user_context[chat_id] = ""
    bot.send_message(message.chat.id, "Контекст разговора очищен")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Если ты хочешь, чтобы я забыл о прошлых темах, напиши команду /clm")
    bot.send_message(message.chat.id, "Если ты хочешь проверить правильное написание английского предложения, напиши: Correct this to standard English:\n\n(два переноса строки)Проверяемое предложение.")
    bot.send_message(message.chat.id, "Если ты хочешь перевести с английского на любой язык, напиши: Translate this into 1. French, 2. Spanish and 3. Japanese(нужные языки):\n\n(два переноса строки)Переводимое предложение.")
    bot.send_message(message.chat.id, "Если ты хочешь перевести с русского на другой язык, напиши: Переведи это с русского на (требуемый язык):\n\n(два переноса строки)Переводимое предложение.")

@bot.message_handler(content_types=["text"])
def handle_message(message):
    try:
        global prompt
        global user_context
        chat_id = message.chat.id
        user_input = message.text
        if chat_id not in user_context:
            user_context[chat_id] = ""
        prompt = user_context[chat_id] + "\nUser: " + user_input
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
        )
        answer = response['choices'][0]['text']
        user_context[chat_id] = prompt + answer
    except:
        bot.polling()
    try:
        bot.send_message(chat_id=message.from_user.id, text=answer)
    except:
        bot.send_message(chat_id=message.from_user.id, text=answer)

try:
    bot.polling()
except:
    bot.polling()