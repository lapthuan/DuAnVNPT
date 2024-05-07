import time
import os
import openpyxl
import requests
import re
import telebot
import sys
import paramiko
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, ReadTimeout
# Load các biến môi trường từ file .env
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


# Lấy thông tin đăng nhập từ biến môi trường
BOT_TOKEN = os.getenv('BOT_TOKEN')
USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')
bot = telebot.TeleBot(BOT_TOKEN)

# Lấy thông tin đăng nhập bras
hostname_bras = os.getenv('HOSTNAME')
user_bras = os.getenv('USER')
password_bras = os.getenv('PASSWORD')

# Định nghĩa các URL cần sử dụng
search_url = os.getenv('SEARCH_URL')
login_url = os.getenv('LOGIN_URL')
doOpenSuspend_url = os.getenv('DO_OPEN_SUSPEND_URL')
detail_url = os.getenv('DETAIL_URL')


def checkBras(userBras):
    try:
        session = paramiko.SSHClient()
        session.load_system_host_keys()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(hostname_bras, username=user_bras, password=password_bras)
      
        # Tạo lệnh kiểm tra
        cmd = f"pwd"
        exit_cmd = f"exit"
       
        # Mở một kênh SSH
        ssh_channel = session.invoke_shell()

        command = 'sho_sub_acc daihostvlgs\n'
        ssh_channel.send(command)

        # Đọc kết quả trả về từ lệnh "sho_sub_acc daihostvlg"
        output = ''
        while not output.endswith('~$ '):  # Đợi cho đến khi nhận được dấu nhắc lệnh trở lại
            output += ssh_channel.recv(1024).decode()

        # In kết quả
        print(output)

        # Đóng kết nối
        session.close()
                
        #Kiểm tra kết quả trả về của bras 1
        if output.strip() == "Total subscribers: 0, Active Subscribers: 0":
            #Thoát khỏi session bras 1
            session.exec_command(exit_cmd)
            time.sleep(0.5)
            session.close()
            return f"Không tìm thấy tài khoản {userBras}"
        
            #Thực hiện kiểm tra trên bras 2
            # session_pre = paramiko.SSHClient()
            # session_pre.load_system_host_keys()
            # session_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # session_pre.connect(hostname_bras_pre, username=user_bras, password=password_bras)

            # stdin, stdout, stderr = session_pre.exec_command(cmd)
            # time.sleep(0.5)
            # output = stdout.read().decode('utf-8')

            #Kiểm tra trên bras 2
            # if output.strip() == "Total subscribers: 0, Active Subscribers: 0":
            #     session_pre.exec_command(exit_cmd)
            #     time.sleep(0.5)
            #     session_pre.close()
            #     return f"Không tìm thấy tài khoản {userBras}"

            #else:
                # Tách kết quả thành các dòng
                #output_lines = output.split('\n')
                
                # Lọc các dòng chứa thông tin cần thiết
                #relevant_lines = [line.strip() for line in output_lines if any(keyword in line for keyword in ['User Name:', 'IP Address:', 'IP Netmask:', 'Primary DNS Address:', 'Secondary DNS Address:', 'Login Time:'])]
                
                #Tách lấy 2 dòng chứa dns
                # dns_address = [line.split(': ')[1].strip() for line in relevant_lines if line.startswith('Primary DNS Address') or line.startswith('Secondary DNS Address')]
                #Kiểm tra dns
                # if '123.26.26.26' not in dns_address or '123.23.23.23' not in dns_address:
                #     return f"Tài khoản {userBras} còn khóa cước Bras"
                
                # Gửi lại các dòng đã lọc cho người dùng
                # session_pre.exec_command(exit_cmd)
                # time.sleep(0.5)
                # session_pre.close()
                # return '\n'.join(relevant_lines)
        else:
             # Tách kết quả thành các dòng
                output_lines = output.split('\n')
                
                # Lọc các dòng chứa thông tin cần thiết
                relevant_lines = [line.strip() for line in output_lines if any(keyword in line for keyword in ['User Name:', 'IP Address:', 'IP Netmask:', 'Primary DNS Address:', 'Secondary DNS Address:', 'Login Time:'])]
                
                #Tách lấy 2 dòng chứa dns
                # dns_address = [line.split(': ')[1].strip() for line in relevant_lines if line.startswith('Primary DNS Address') or line.startswith('Secondary DNS Address')]
                #Kiểm tra dns
                # if '123.26.26.26' not in dns_address or '123.23.23.23' not in dns_address:
                #     return f"Tài khoản {userBras} còn khóa cước Bras"
                
                # Gửi lại các dòng đã lọc cho người dùng
                session.exec_command(exit_cmd)
                time.sleep(0.5)
                session.close()
                return "'\n'.join(relevant_lines)"
    except Exception as err:
        print(str(err))
        return "Fail"

checkBras("daihostvlg")