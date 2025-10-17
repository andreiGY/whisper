import sqlite3

def get_data():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audio_file TEXT NOT NULL,
                output_file TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        ''')
    conn.commit()
    cursor.execute("SELECT audio_file, output_file, datetime FROM history")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
    
    

def save_data(audio_file, output_file, datetime):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audio_file TEXT NOT NULL,
                output_file TEXT NOT NULL,
                datetime TEXT NOT NULL
            )
        ''')
    conn.commit()
    cursor.execute("INSERT INTO history (audio_file, output_file, datetime) VALUES (?, ?, ?)", (audio_file, output_file, datetime))
    conn.commit()
    cursor.close()
    conn.close()
    return