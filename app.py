import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = "8894849933:AAGnHR_WqLny6JeW4201HAKRMu1OpEl7ESs"
CHAT_ID = "7651507310"

@app.route('/webhook', methods=['POST'])
def handle_form():
    data = request.form
    
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
    requests.post(url, json=payload)
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))