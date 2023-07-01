from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import openpyxl
from openpyxl.styles import Alignment, Font
from dotenv import load_dotenv
from pathlib import Path
import telebot
from datetime import datetime
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


BOT_TOKEN = os.getenv('BOT_TOKEN')
USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')
bot = telebot.TeleBot(BOT_TOKEN)
options = webdriver.ChromeOptions()

# options.add_argument('--headless')
options.add_experimental_option("detach", True)
# Biến kiểm tra đã đăng nhập hay chưa


def login(username,user):
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.get('http://10.156.7.25/visa/login.vnpt')

        taikhoan = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/form/table/tbody/tr[3]/td/input')
        taikhoan.send_keys(USERNAME)

        matkhau = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/form/table/tbody/tr[5]/td/input')
        matkhau.send_keys(PASSWORD)

        dangnhap = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td/div/table/tbody/tr/td[2]/div/div/form/table/tbody/tr[6]/td/input')
        dangnhap.click()

   
        select = driver.find_element(By.CSS_SELECTOR, "span.title")
        hover = ActionChains(driver).move_to_element(select)
        hover.perform()

        time.sleep(.5)

        tracuu = driver.find_element("xpath", '/html/body/div[1]/div[2]/header/div[1]/nav/ul/li[1]/ul/li[1]/a')
        tracuu.click()
        
        uservisa = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/fieldset/form/table/tbody/tr[10]/td[2]/input')
        uservisa.send_keys(username)
        
        timkiem = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/fieldset[1]/form/table/tbody/tr[18]/td[2]/input[1]')
        timkiem.click()

        time.sleep(.5)

        div_elementTimKiem = driver.find_element(By.CSS_SELECTOR, 'div.line.left.color1')

        textTimKiem = div_elementTimKiem.text

        if textTimKiem == "Tổng số kết quả trả về:  0":
            driver.close()
            return "Không tìm thấy tài khoản"

        radio = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/fieldset[2]/table/tbody/tr/td[2]/input')
        radio.click()

        time.sleep(1)

        motamngung = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/div[2]/input[11]')
        if motamngung.is_displayed():
        
            motamngung.click()
            
            ghichu = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/form/fieldset[2]/table/tbody/tr/td[2]/textarea')
            ghichustring = "Bot telegram mở cước, User yêu cầu : {}".format(user)
            ghichu.send_keys(ghichustring)  
                
            thuchien = driver.find_element("xpath", '/html/body/div[1]/table/tbody/tr/td[2]/div/form/div/input[1]')
            thuchien.click()
            
            time.sleep(1)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.alert_is_present())
           
            al = driver.switch_to.alert
            al.accept()

            time.sleep(.5)

            driver.close()
            return "Mở cước thành công"
        else:
            driver.close()
            return "Tài khoản đang được kích hoạt"
      
    except:
        driver.close()
        return "Lỗi"
      
        

   
    
  
    
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
    
    username = message.text.replace('/mc', '').strip()
    bot.reply_to(message, f"Đang thực hiện mở khóa tài khoản: {username}")
    user = message.from_user.full_name

    # print(username)
    # Kiểm tra xem đã đăng nhập hay chưa
    
    if USERNAME and PASSWORD:
        status = login(username,user)
     
        bot.reply_to(message, status)
        thoigian = message.date
        formatted_time = datetime.fromtimestamp(thoigian).strftime('%Y-%m-%d %H:%M:%S')
        formatted_time = formatted_time.encode('ascii', 'replace').decode('ascii')
        formatted_data = f"Người thực hiện: {user}, Tài khoản mở cước: {username} , Thời gian: {formatted_time}, Phản hồi: {status}"
        with open('du_lieu.txt', 'a', encoding='utf-8') as file:
            file.write(formatted_data + "\n")

           # Đường dẫn tới file văn bản
        path_to_txt = 'du_lieu.txt'

        # Tạo một workbook mới
        workbook = openpyxl.Workbook()

        # Chọn sheet đầu tiên
        sheet = workbook.active

        # Đọc dữ liệu từ file văn bản và ghi vào sheet
        with open(path_to_txt, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for row, line in enumerate(lines, start=2):
            # Tách các giá trị trong dòng văn bản
            values = line.strip().split(',')

            # Ghi dữ liệu vào các cột tùy chỉnh
            for col, value in enumerate(values, start=1):
                sheet.cell(row=row, column=col, value=value)

        # Tùy chỉnh tiêu đề "Bảng Thống Kê"
        title_cell = sheet['A1']
        title_cell.value = 'Bảng Thống Kê'
        title_cell.font = Font(size=13)
        title_cell.alignment = Alignment(horizontal='center')
        sheet.merge_cells('A1:D1')


        # Lưu workbook thành file Excel
        desktop_path = os.path.expanduser("~/Desktop")
        file_name = "du_lieu.xlsx"
        path_to_excel = os.path.join(desktop_path, file_name)
        workbook.save(path_to_excel)
        
 


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
