import sqlite3

def get_data():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audio_file TEXT NOT NULL,
                output_file TEXT NOT NULL,
                datetime TEXT NOT NULL,
                model_name TEXT NOT NULL,
                device TEXT NOT NULL
            )
        ''')
    conn.commit()
    cursor.execute("SELECT audio_file, output_file, datetime, model_name, device  FROM history")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows
    
    

def save_data(audio_file, output_file, datetime, model_name, device):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audio_file TEXT NOT NULL,
                output_file TEXT NOT NULL,
                datetime TEXT NOT NULL,
                model_name TEXT NOT NULL,
                device TEXT NOT NULL
            )
        ''')
    conn.commit()
    cursor.execute("INSERT INTO history (audio_file, output_file, datetime, model_name, device) VALUES (?, ?, ?, ?, ?)", (audio_file, output_file, datetime, model_name, device))
    conn.commit()
    cursor.close()
    conn.close()
    return