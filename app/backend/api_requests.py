import json
import time
import hmac
import hashlib
import base64
import requests
import os
from aiogram.types import User  # Импорт из aiogram
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "123")
URL = os.getenv("API_URL", "http://0.0.0.0:8000/")


def generate_signature(data, secret_key):
    """
    Генерация HMAC-SHA256 подписи с сортировкой тела запроса
    """
    sorted_data = json.dumps(data, separators=(
        ',', ':'), sort_keys=True).encode('utf-8')
    signature = hmac.new(secret_key.encode('utf-8'),
                         sorted_data, hashlib.sha256).digest()
    return base64.b64encode(signature).decode('utf-8')


def send_signed_request(user: User, uuid: str, path: str = "service/confirm-code/", referred_by: str = None):
    """
    Формирует тело запроса с подписью и отправляет его на сервер
    """
    data = {
        "uuid": uuid,
        "chat_id": user.id,
        "username": user.username or "Нет username",
        "full_name": user.full_name,
        "is_premium": user.is_premium if hasattr(user, 'is_premium') else False,
        "language_code": user.language_code,
        "timestamp": int(time.time()),
        "referred_by": referred_by
    }

    # Генерация подписи
    data['signature'] = generate_signature(data, SECRET_KEY)

    # Вывод подготовленного запроса
    print("\nГотовое тело запроса:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # Отправка запроса
    response = requests.post(URL + path, json=data)

    print("\nРезультат запроса:")
    if response.status_code == 200:
        pass
    else:
        print("Ошибка:", response.status_code, response.text)

    return response.status_code
