import subprocess
from config import TELEGRAM_API_URL, TELEGRAM_CHAT_ID


def send_telegram_message(log_message):
    try:
        command = [
            'curl',
            '-X', 'POST',
            TELEGRAM_API_URL,
            '-d', f'chat_id={TELEGRAM_CHAT_ID}&text={log_message}'
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        with open('error_log.txt', 'a') as f:
            f.write(str(e) + '\n')
