import os
import subprocess

base_dir = '/home/easy_refer_bot'
script_name = 'aiogram_run.py'
script_path = os.path.join(base_dir, script_name)

if os.path.exists(script_path):
    subprocess.run(['/home/easy_refer_bot/venv/bin/python3', script_path], check=True)
else:
    print("Не удалось найти скрипт aiogram_run.py.")