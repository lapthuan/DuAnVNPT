import os
import telebot

bot = telebot.TeleBot('6375060028:AAEhRDGtZKPUgynEGmPGPP8TMrBScn2pQ88')


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Ok đây là phản hồi")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling()
