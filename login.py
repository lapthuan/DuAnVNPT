import requests
import os
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from urllib.parse import urlencode
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
search_url = 'http://10.156.7.25/visa/package/customer.vnpt'
login_url = 'http://10.156.7.25/visa/j_spring_login.vnpt'
USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')

session = requests.Session()

login_data = {
    'j_username': USERNAME,
    'j_password': PASSWORD
}

# Mã hóa dữ liệu thành x-www-form-urlencoded
encoded_login_data = urlencode(login_data)

response = session.post(login_url, data=encoded_login_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
cookies = session.cookies.get_dict()

cookies_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

# print(cookies_str)


account_name = 'daihostvlg'
m = 'getList'
typeAction = "LIST"
organizationId = "64"
search_data = {
    'bean.serviceInfo.account': account_name,
    'm': m,
    "typeAction": typeAction,
    "bean.organizationId": organizationId
}
# Tạo đối tượng MultipartEncoder để định dạng dữ liệu thành multipart/form-data
multipart_data = MultipartEncoder(fields=search_data)

response_search = session.post(search_url, data=multipart_data, headers={'Content-Type': multipart_data.content_type, 'Cookie': cookies_str})

soup = BeautifulSoup(response_search.text, 'html.parser')

# Lấy giá trị 'bean.id' từ href thứ nhất
first_a_tag = soup.find('a', href=re.compile(r'bean\.id=\d+'))
if first_a_tag:
    href = first_a_tag['href']
    bean_id = re.search(r'bean\.id=(\d+)', href).group(1)
    print('bean.id (first):', bean_id)
else:
    print('Không tìm thấy thẻ <a> chứa bean.id')

# Lấy giá trị 'bean.id' từ href thứ hai
second_a_tag = soup.find('a', href=re.compile(r'bean\.id=\d+', re.I))
if second_a_tag:
    href = second_a_tag['href']
    bean_id = re.search(r'bean\.id=(\d+)', href).group(1)
    print('bean.id (second):', bean_id)
else:
    print('Không tìm thấy thẻ <a> chứa bean.id')