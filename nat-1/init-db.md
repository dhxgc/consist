## Комментарий по поводу инициализации флага в БД

1. `init_db()` - добавляет флаг и шифрует его.
2. Было это сделано для того, чтобы добавить флаг. Дальше сервис будет без этой функции

> На всякий содержимое функции

```python
c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  content TEXT,
                  timestamp DATETIME)''')

    # Шифруем флаг для проверки
    flag = "flag{This is not the end yet! =)}"
    encrypted_flag = encrypt_data(flag)  # Используем ту же функцию шифрования
    
    # Проверяем существование именно ЗАШИФРОВАННОГО флага
    c.execute("SELECT content FROM messages WHERE content = ?", (encrypted_flag,))
    
    if not c.fetchone():
        c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)",
                 (encrypted_flag, datetime.now()))
    
    conn.commit()
    conn.close()
```
