# -*- coding: utf-8 -*-
from os import name
import telebot
from telebot import *

bot = telebot.TeleBot('7706937394:AAEO4HWY8RubKHlnQbJRL51zVhThg89Du0o') 

@bot.message_handler(commands = ['start'])
def start(messsage):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttonOne = types.KeyboardButton('О боте (info)')
    buttonTwo = types.KeyboardButton('Список задач')
    buttonThree = types.KeyboardButton('Описание задачи')
    buttonFour = types.KeyboardButton('Обновить список задач')
    buttonFive = types.KeyboardButton('Авторизироваться на сайте LMS')
    markup.row(buttonOne,buttonTwo,buttonThree)
    markup.row(buttonFour,buttonFive)

    bot.send_message(messsage.chat.id, 'Добро пожаловать в бота!', reply_markup=markup)

    


bot.polling(none_stop=True) # Непрерывность выполнения программы



