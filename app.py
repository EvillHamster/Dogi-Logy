import os
import threading
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = "8897054825:AAEXw76yW_aK0xoBO782TaUOES3KS2QCoDQ"
CHAT_ID = "1305714512"

def send_to_telegram(data):
    try:
        form_title = data.get('form_title')
        
        if form_title:
            message = f"*{form_title}*\n\n"
        else:
            message = ""
        
        # Получаем значение согласия
        consent_value = data.get('Consent')
        
        # Проверяем все возможные варианты "Да"
        if consent_value in ('yes', 'on', '1', 'true', 'True', 'YES', 'ON'):
            consent_display = 'Да'
        elif consent_value:
            consent_display = consent_value  # если пришло что-то другое
        else:
            consent_display = None  # если поля нет
        
        fields = {
            '📞 Телефон': 'Phone',
            '👤 Имя': 'Name',
            '💬 Где с вами связаться?': 'Social',
            '💰 Тариф': 'Tariff',
            '📝 Текст сообщения': 'Text',
            '✍️ Расскажите о себе': 'About'
        }
        
        # Согласие добавляем только если оно есть
        if consent_display:
            fields['✅ Согласие на обработку'] = consent_display
        
        for label, key in fields.items():
            if isinstance(key, str):
                value = data.get(key)
            else:
                value = key
            
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
    
    # ОТЛАДКА
    print("=== ВСЕ ПОЛЯ ИЗ ТИЛЬДЫ ===")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("============================")
    
    thread = threading.Thread(target=send_to_telegram, args=(data,))
    thread.start()
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
