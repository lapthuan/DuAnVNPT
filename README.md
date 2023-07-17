# DuAnVNPT

## Thao Tác

### Cài thư viện

```shell
pip install selenium
pip install pyinstaller
```

### Tạo file .env

BOT_TOKEN = 

VISA_USERNAME= anvlg

VISA_PASSWORD= S*8Jw7$@@L#0

SEARCH_URL = 'http://10.156.7.25/visa/package/customer.vnpt'

LOGIN_URL = 'http://10.156.7.25/visa/j_spring_login.vnpt'

DO_OPEN_SUSPEND_URL = 'http://10.156.7.25/visa/package/customer.vnpt?m=doOpenSuspend'

DETAIL_URL= 'http://10.156.7.25/visa/package/customer.vnpt?m=detail&bean.id='


/etc/supervisor/conf.d/auto_visa_conf.conf
[program:auto_visa]
command=/home/hostvlg/DuAnVNPT/venv/bin/python -u service.py
directory=/home/hostvlg/DuAnVNPT
stdout_logfile=/home/hostvlg/DuAnVNPT/auto_visa_output.txt
redirect_stderr=true

sudo supervisorctl
reread
add auto_visa
restart auto_visa
status