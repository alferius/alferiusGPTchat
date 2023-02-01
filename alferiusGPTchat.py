#create chat GPT telegramm bot from python  

import os
import openai
from dotenv import load_dotenv
import telebot

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
prompt = ""
model = "text-davinci-003"
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_answer(prompt, model):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )


    #if response.status_code == 200:
    response_text = response['choices'][0]['text']
    return response_text
    #else:
    #    return "Error: " + str(response.status_code)

bot = telebot.TeleBot(os.getenv('TELEGRAM_API_KEY'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я чатбот основанный на OpenAI. Спроси меня что нибудь или напиши команду /help.")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Если ты хочешь проверить правильное написание английского предложения, напиши: Correct this to standard English:\n\n(два переноса строки)Проверяемое предложение.")
    bot.send_message(message.chat.id, "Если ты хочешь перевести с английского на любой язык, напиши: Translate this into 1. French, 2. Spanish and 3. Japanese(нужные языки):\n\n(два переноса строки)Переводимое предложение.")
    bot.send_message(message.chat.id, "Если ты хочешь перевести с русского на другой язык, напиши: Переведи это с русского на (требуемый язык):\n\n(два переноса строки)Переводимое предложение.")

@bot.message_handler(content_types=["text"])
def chat(message):
    global prompt
    user_input = message.text
    prompt = prompt + "\nUser: " + user_input
    answer = generate_answer(prompt, model)
    prompt = prompt + "\nChatGPT: " + answer
    bot.send_message(message.chat.id, answer)

bot.polling()
