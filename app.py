import os
import threading
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = "8894849933:AAGnHR_WqLny6JeW4201HAKRMu1OpEl7ESs"
CHAT_ID = "7651507310"

def send_to_telegram(data):
    try:
        form_title = data.get('form_title')
        
        if form_title:
            message = f"*{form_title}*\n\n"
        else:
            message = ""
        
        fields = {
            '📞 Телефон': 'Phone',
            '👤 Имя': 'Name',
            '💬 Где с вами связаться?': 'Social',
            '💰 Тариф': 'Tariff',
            '📝 Текст сообщения': 'Text',
            '✍️ Расскажите о себе': 'About',
            '✅ Согласие на обработку': 'Consent'
        }
        
        for label, key in fields.items():
            value = data.get(key)
            if value:
                message += f"{label}: {value}\n"
        
        if not message.strip():
            print("Нет данных для отправки")
            return
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        requests.post(url, json=payload, timeout=15)
        print(f"Сообщение отправлено: {form_title}")
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")

@app.route('/webhook', methods=['POST', 'GET'])
def handle_form():
    if request.method == 'GET':
        return 'Webhook is working', 200
    
    data = request.form
    thread = threading.Thread(target=send_to_telegram, args=(data,))
    thread.start()
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
