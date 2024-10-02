import sqlite3

def init_db():
    conn = sqlite3.connect('car_wash.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        phone TEXT,
        registered_on DATE
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS services (
        service_id INTEGER PRIMARY KEY,
        service_name TEXT,
        service_price REAL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS time_slots (
        slot_id INTEGER PRIMARY KEY,
        date TEXT,
        time TEXT,
        is_available BOOLEAN
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        service_id INTEGER,
        slot_id INTEGER,
        booked_on DATE,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(service_id) REFERENCES services(service_id),
        FOREIGN KEY(slot_id) REFERENCES time_slots(slot_id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
        admin_id INTEGER PRIMARY KEY
    )''')
    conn.commit()
    conn.close()

