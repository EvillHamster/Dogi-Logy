import os
import threading
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = "8894849933:AAGnHR_WqLny6JeW4201HAKRMu1OpEl7ESs"
CHAT_ID = "7651507310"

def send_to_telegram(data):
    """Отправляет данные в Telegram в фоновом потоке"""
    try:
        message = (
            "📋 *Новая заявка с сайта*\n\n"
            f"📞 Телефон: {data.get('Phone', 'Не указан')}\n"
            f"👤 Имя: {data.get('Name', 'Не указано')}\n"
            f"💬 Соцсеть: {data.get('Social', 'Не указана')}\n"
            f"✍️ Запрос: {data.get('Text', 'Не указан')}\n"
            f"✅ Согласие: {data.get('Consent', 'Нет')}"
        )
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        # Таймаут 10 секунд, чтобы не висеть вечно
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

@app.route('/webhook', methods=['POST', 'GET'])
def handle_form():
    # Для проверки GET-запросов (Тильда проверяет доступность)
    if request.method == 'GET':
        return 'Webhook is working', 200
    
    # Получаем данные из формы
    data = request.form
    
    # Запускаем отправку в Telegram в фоновом потоке
    thread = threading.Thread(target=send_to_telegram, args=(data,))
    thread.start()
    
    # Сразу возвращаем ответ, чтобы не держать Тильду
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))