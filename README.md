# DuAnVNPT

## Thao Tác

### Cài thư viện

```shell
pip install selenium
pip install pyinstaller
```

### Tạo file .env

BOT_TOKEN = 6375060028:AAEhRDGtZKPUgynEGmPGPP8TMrBScn2pQ88
VISA_USERNAME= anvlg
VISA_PASSWORD= S*8Jw7$@@L#0

### Thay đổi cấu hình

Trước khi thực hiện, bạn có thể tùy chỉnh các thông số sau:

- Để ẩn trình duyệt khi thực hiện, hãy mở dòng `options.add_argument('--headless')`.

- Để thay đổi đường dẫn trang web, hãy sửa đổi giá trị của biến `Link`.

- Để thay đổi XPath của ô nhập tài khoản, làm theo các bước sau:

  1. Bật trình duyệt và truy cập vào trang web.
  2. Sử dụng phím tắt F12 để mở cửa sổ Developer Tools.
  3. Tìm đến ô nhập tài khoản trên trang web.
  4. Chuột phải vào ô nhập tài khoản và chọn "Copy" hoặc "Copy full XPath".
  5. Thay thế giá trị của biến `xpath_input_username` bằng XPath được sao chép.

- Để thay đổi XPath của ô nhập mật khẩu, làm tương tự như trên và thay thế giá trị của biến `xpath_input_password`.

- Để thay đổi XPath của nút đăng nhập, làm tương tự như trên và thay thế giá trị của biến `xpath_button_login`.

Chú ý: Đảm bảo rằng bạn đã cài đặt đúng các thư viện và đã thực hiện các thay đổi cần thiết trước khi chạy mã.
