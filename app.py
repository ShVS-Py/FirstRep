import requests
import json
import telebot

TOKEN = "7092152794:AAG5I8AGX1qcjFrEUFRl7n4hqgDdjuoFufo"

bot = telebot.TeleBot(TOKEN)

keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD'
}

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<наименование валюты> \
<наименование валюты, в которую переводим> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    quote, base, amount = message.text.split(' ')
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsyms={keys[quote]}&tsyms={keys[base]}')
    text = json.loads(r.content)[keys[base]]
    bot.send_message(message.chat.id, text)

bot.polling()
