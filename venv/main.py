from mailbox import Message
import telebot
from telebot import types
from jikanpy import Jikan
from telebot.types import InlineKeyboardMarkup
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message: Message):
    bot.send_message(message.chat.id, 'Привет, я аниме бот \n'
                                      'Введите команду /help для получения большей информации')


@bot.message_handler(commands=['help'])
def command_handler(message: Message):
    bot.send_message(message.chat.id,
                     'Я бот с быстрым доступом к сайту MyAnimeList.net! \n'
                     'Введите название аниме: Например naruto')


@bot.message_handler(content_types=['text'])
def repeat_all_messages(message):
    request = message.text
    jikan = Jikan()
    apiResult = jikan.search('anime', request)
    listResult = apiResult['results'][:5]
    keyboard: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    for item in listResult:
        btn = types.InlineKeyboardButton(text=item['title'], url=item['url'])
        keyboard.add(btn)
    if not listResult:
         bot.send_message(message.chat.id, "Ошибка, введите название аниме:")
    else:
        bot.send_message(message.chat.id, 'Нажми на кнопку и перейди по ссылки.', reply_markup=keyboard)



# RUN
bot.polling(none_stop=True)