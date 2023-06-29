from selenium import webdriver

options = webdriver.ChromeOptions()

# options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get('https://facebook.com')

taikhoan = driver.find_element("xpath",'/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input')
taikhoan.send_keys('taikhoan')

matkhau = driver.find_element("xpath",'/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input')
matkhau.send_keys('matkhau')

dangnhap = driver.find_element("xpath",'/html/body/div[1]/div[1]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
dangnhap.click()
