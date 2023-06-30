from selenium import webdriver
import time
import os
import telebot

bot = telebot.TeleBot('6375060028:AAEhRDGtZKPUgynEGmPGPP8TMrBScn2pQ88')
options = webdriver.ChromeOptions()

# options.add_argument('--headless')

# Biến kiểm tra đã đăng nhập hay chưa
is_logged_in = False

# Biến lưu giữ tài khoản và mật khẩu
username = ''
password = ''

def login():
    global is_logged_in, username, password
    
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.luxubu.shop/Login')

    taikhoan = driver.find_element("xpath", '/html/body/div/div[1]/div[2]/div/div[2]/div/form/input')
    taikhoan.send_keys(username)

    matkhau = driver.find_element("xpath", '/html/body/div/div[1]/div[2]/div/div[2]/div/form/span/input')
    matkhau.send_keys(password)

    dangnhap = driver.find_element("xpath", '/html/body/div/div[1]/div[2]/div/div[2]/div/form/button')
    dangnhap.click()

    # Đánh dấu đã đăng nhập thành công
    is_logged_in = True

    # Đợi một thời gian để đảm bảo đăng nhập thành công
    time.sleep(5)

# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Ok đây là phản hồi")

@bot.message_handler(commands=['username'])
def set_username(message):
    global username
    username = message.text.replace('/username', '').strip()
    bot.reply_to(message, f"Tài khoản đã được cập nhật: {username}")

@bot.message_handler(commands=['password'])
def set_password(message):
    global password
    password = message.text.replace('/password', '').strip()
    bot.reply_to(message, "Mật khẩu đã được cập nhật!")

@bot.message_handler(commands=['login'])
def login_command(message):
    global is_logged_in, username, password
    
    # Kiểm tra xem đã đăng nhập hay chưa
    if not is_logged_in:
        if username and password:
            login()
            bot.reply_to(message, "Đăng nhập thành công!")
        else:
            bot.reply_to(message, "Vui lòng cung cấp tài khoản và mật khẩu trước!")
    else:
        bot.reply_to(message, "Bạn đã đăng nhập rồi!")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
