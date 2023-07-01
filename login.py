from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from pathlib import Path
import telebot

dotenv_path = Path('D:\\vnpt\\DuAnVNPT\\.env')
load_dotenv(dotenv_path=dotenv_path)


BOT_TOKEN = os.getenv('BOT_TOKEN')
USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')
bot = telebot.TeleBot(BOT_TOKEN)
options = webdriver.ChromeOptions()

# options.add_argument('--headless')
options.add_experimental_option("detach", True)
# Biến kiểm tra đã đăng nhập hay chưa
is_logged_in = False

# Biến lưu giữ tài khoản và mật khẩu
username = ''


def login(username,user):
    global is_logged_in
    
    driver = webdriver.Chrome(options=options)
    driver.get('http://10.156.7.25/visa/login.vnpt')

    taikhoan = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/form/table/tbody/tr[3]/td/input')
    taikhoan.send_keys(USERNAME)

    matkhau = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/form/table/tbody/tr[5]/td/input')
    matkhau.send_keys(PASSWORD)

    dangnhap = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/form/table/tbody/tr[6]/td/input')
    dangnhap.click()

    # Đánh dấu đã đăng nhập thành công
    is_logged_in = True

    # Đợi một thời gian để đảm bảo đăng nhập thành công
    select = driver.find_element(By.CSS_SELECTOR, "span.title")
    hover = ActionChains(driver).move_to_element(select)
    hover.perform()
    
    time.sleep(1)
    tracuu = driver.find_element("xpath", '/html/body/div[1]/div[2]/header/div[1]/nav/ul/li[1]/ul/li[1]/a')
    tracuu.click()
    
    uservisa = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/fieldset/form/table/tbody/tr[10]/td[2]/input')
    uservisa.send_keys(username)
    
    timkiem = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/fieldset[1]/form/table/tbody/tr[18]/td[2]/input[1]')
    timkiem.click()
    
    radio = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/fieldset[2]/table/tbody/tr/td[2]/input')
    radio.click()
    time.sleep(1)
    
    motamngung = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/div[2]/input[11]')
    motamngung.click()
    
    time.sleep(1)
    
    ghichu = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/form/fieldset[2]/table/tbody/tr/td[2]/textarea')
    ghichustring = "bot telegram mở cước, User yêu cầu : {}".format(user)
    ghichu.send_keys(ghichustring)
    time.sleep(1)
    
        
    thuchien = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/form/div/input[1]')
    thuchien.click()
    
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    driver.switch_to.alert.accept()
    
    time.sleep(5)

    # dangxuat = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[1]/div[1]/div/div[2]/input')
    # dangxuat.click()
    
  
    
# @bot.message_handler(commands=['start', 'hello'])
# def send_welcome(message):
#     bot.reply_to(message, "Ok đây là phản hồi")

# @bot.message_handler(commands=['username'])
# def set_username(message):
#     global username
#     username = message.text.replace('/username', '').strip()
#     bot.reply_to(message, f"Tài khoản đã được cập nhật: {username}")

# @bot.message_handler(commands=['password'])
# def set_password(message):
#     global password
#     password = message.text.replace('/password', '').strip()
#     bot.reply_to(message, "Mật khẩu đã được cập nhật!")

@bot.message_handler(commands=['mc'])
def login_command(message):
    global is_logged_in, username
    username = message.text.replace('/mc', '').strip()
    bot.reply_to(message, f"Đang thực hiện mở khóa tài khoản: {username}")
    user = message.from_user.full_name

    # print(username)
    # Kiểm tra xem đã đăng nhập hay chưa
    
    if USERNAME and PASSWORD:
        login(username,user)
        bot.reply_to(message, "Mở thành công!")
 


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
