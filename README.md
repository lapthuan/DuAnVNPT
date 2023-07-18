# DuAnVNPT

## Thao Tác

### Tạo file .env

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
