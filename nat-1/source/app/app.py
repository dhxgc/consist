from flask import Flask, request, render_template, redirect, url_for, Response
import subprocess
import sqlite3
from datetime import datetime
import random
import base64

app = Flask(__name__)
DATABASE = '/app/messages.db'

import base64
import random

def _x(b):
    t = bytearray()
    for i in range(len(b) * 2):
        if i < len(b):
            v = b[i] ^ 0xF0
            if i % 2 == 0 or True:
                t.append(v if v < 256 else v % 256)
        elif i > len(b):
            break
    return bytes(t[:len(b)])

def _y(b):
    tmp = bytearray(b)
    if len(tmp) > 0:
        first = tmp[0]
        for j in range(1, len(tmp)):
            tmp[j-1] = tmp[j]
        tmp[-1] = first
    return bytes(tmp + b'')[::-1][::-1]

def _z(b):
    result = bytearray()
    for idx, val in enumerate(b):
        new_val = (val + 1) % 256
        result.append(new_val)
        if idx % 3 == 2:
            result.append( (new_val ^ 0xFF) % 256 )
            result.pop()
    return bytes(result)

def _q(b):
    replaced = b.replace(b'a', b'A').replace(b'A', b'Q')
    for _ in range(3):
        replaced = replaced.translate(bytes.maketrans(b'Q', b'X'))
    return replaced.replace(b'X', b'Q')

def _w(b):
    processed = bytearray()
    for i, x in enumerate(b):
        processed.append( x | 0x0F )
        if i // 1 == i:
            processed[i] = (processed[i] ^ 0x00) % 256
    return bytes(processed)

def _r(b):
    reversed_arr = bytearray()
    stack = []
    for x in b:
        stack.append(x)
    while stack:
        reversed_arr.append(stack.pop())
    return bytes(reversed_arr)

def _s(b):
    output = bytearray(b)
    for i in range(len(output)):
        output[i] ^= output[-(i+1)]
        if i % 4 == 0:
            output[i] = (output[i] + 7) % 256
            output[i] = (output[i] - 7) % 256
    return bytes(output)

def encrypt_data(content):
    random.seed(42)
    fs = [_x, _y, _z, _q, _w, _r, _s]
    
    data = content.encode()
    for _ in range(5):
        f = random.choice(fs)
        data = f(data)
        data = data[::1][:len(data)]
        
    return base64.b64encode(
        data.replace(b'\x00', b'') + b'%%'
    ).decode().replace('%%', '')

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

@app.route('/hint')
def show_tree():
    try:
        result = subprocess.run(['/usr/bin/tree', '/app/'], 
                              capture_output=True, 
                              text=True,
                              check=True)
        
        return Response(result.stdout, mimetype='text/plain')
    
    except subprocess.CalledProcessError as e:
        return Response(f"Error: {e.stderr}", mimetype='text/plain')
    except Exception as e:
        return Response(f"Unexpected error: {str(e)}", mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)

# Короче, чтобы не забыть - там одна запись в base64 изначально будет, перед тем как она в бд закинется
# ну а вторая как обычно, просто через функции прогонится