# app.py
from flask import Flask, render_template, request
import json
import os
import time

app = Flask(__name__)

# Константы
TOKENS_FILE = 'tokens.json'

def load_tokens():
    """Загружает токены из файла JSON"""
    if not os.path.exists(TOKENS_FILE):
        return []
    
    try:
        with open(TOKENS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tokens(tokens):
    """Сохраняет токены в файл JSON"""
    try:
        with open(TOKENS_FILE, 'w') as f:
            json.dump(tokens, f, indent=2)
        return True
    except IOError:
        return False

@app.route('/')
def home():
    tokens = load_tokens()
    return render_template('index.html', tokens=tokens)

@app.route('/submit', methods=['GET', 'POST'])
def submit_token():
    if request.method == 'POST':
        # Валидация обязательных полей
        required_fields = ['name', 'symbol', 'chain', 'launch', 'link']
        if not all(field in request.form for field in required_fields):
            return render_template('submit.html', error="Все поля обязательны для заполнения")
        
        new_token = {
            "name": request.form['name'].strip(),
            "symbol": request.form['symbol'].strip().upper(),
            "chain": request.form['chain'].strip(),
            "launch": request.form['launch'].strip(),
            "link": request.form['link'].strip()
        }
        
        tokens = load_tokens()
        tokens.append(new_token)
        
        if save_tokens(tokens):
            return home()
        else:
            return render_template('submit.html', error="Ошибка при сохранении токена")
    
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)