from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = '/app/messages.db'

def encrypt_data(content):
    d = content[::-1]
    key = 0xAA >> 1
    t = []
    for idx, ch in enumerate(d):
        z = ord(ch) ^ key
        z = (z + idx) % 0x100
        t.append(z)
    import base64
    return base64.b64encode(bytes(t)).decode('utf-8')

# def init_db():
#     conn = sqlite3.connect(DATABASE)
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS messages
#                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   content TEXT,
#                   timestamp DATETIME)''')

#     # Шифруем флаг для проверки
#     flag = "flag{This is not the end yet! =)}"
#     encrypted_flag = encrypt_data(flag)  # Используем ту же функцию шифрования
    
#     # Проверяем существование именно ЗАШИФРОВАННОГО флага
#     c.execute("SELECT content FROM messages WHERE content = ?", (encrypted_flag,))
    
#     if not c.fetchone():
#         c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)",
#                  (encrypted_flag, datetime.now()))
    
#     conn.commit()
#     conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            encrypted_content = encrypt_data(content)
            c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)",
                     (encrypted_content, datetime.now()))
            conn.commit()
    
    c.execute("SELECT content, timestamp FROM messages ORDER BY timestamp DESC")
    messages = [{'text': row[0], 'time': datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')} for row in c.fetchall()]
    
    conn.close()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    # init_db()
    app.run(host='127.0.0.1', debug=True)