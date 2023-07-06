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
doOpenSuspend_url = 'http://10.156.7.25/visa/package/customer.vnpt?m=doOpenSuspend'

USERNAME = os.getenv('VISA_USERNAME')
PASSWORD = os.getenv('VISA_PASSWORD')

session = requests.Session()

login_data = {
    'j_username': USERNAME,
    'j_password': PASSWORD
}

encoded_login_data = urlencode(login_data)

response = session.post(login_url, data=encoded_login_data, headers={
                        'Content-Type': 'application/x-www-form-urlencoded'})
cookies = session.cookies.get_dict()

cookies_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])

account_name = 'daihostvlg'
m = 'getList'
typeAction = "LIST"
organizationId = "64"
hierarchy = "on"
search_data = {
    'bean.serviceInfo.account': account_name,
    'm': m,
    "typeAction": typeAction,
    "bean.organizationId": organizationId,
    "bean.hierarchy": hierarchy
}

multipart_data = MultipartEncoder(fields=search_data)

response_search = session.post(search_url, data=multipart_data, headers={
                               'Content-Type': multipart_data.content_type, 'Cookie': cookies_str})

soup = BeautifulSoup(response_search.text, 'html.parser')

first_a_tag = soup.find('a', href=re.compile(r'bean\.id=\d+'))
if first_a_tag:
    href = first_a_tag['href']
    bean_id = re.search(r'bean\.id=(\d+)', href).group(1)
    url_detail = f'http://10.156.7.25/visa/package/customer.vnpt?m=detail&bean.id={bean_id}'

    response_search_detail = session.get(
        url_detail, headers={'Cookie': cookies_str})

    soup2 = BeautifulSoup(response_search_detail.text, 'html.parser')

    # Tìm thẻ <input> với name là "bean.customer.code"
    input_tag = soup2.find('input', attrs={'name': 'bean.customer.code'})

    if input_tag:
        id_user = input_tag['value']

        description = "Bot telegram mở cước, User yêu cầu : {}".format("Test")

        openSuspend_data = {
            "bean.id": bean_id,
            "bean.customer.code": id_user,
            "bean.description": description
        }
        print(openSuspend_data)
        multipart_openSuspend_data = MultipartEncoder(fields=openSuspend_data)

        response_openSuspend = session.post(doOpenSuspend_url, data=multipart_openSuspend_data, headers={
            'Content-Type': multipart_openSuspend_data.content_type, 'Cookie': cookies_str})

        print("Mở cước thành công")
    else:
        print('Không tìm thấy thẻ <input> có name là "bean.customer.code"')

else:
    print('Không tìm thấy thẻ <a> chứa bean.id')
