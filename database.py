# database.py
import sqlite3
from config import DB_PATH

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        phone TEXT,
        registered_on DATE
    )''')
    
    # Таблица услуг
    cursor.execute('''CREATE TABLE IF NOT EXISTS services (
        service_id INTEGER PRIMARY KEY,
        service_name TEXT,
        service_price REAL
    )''')
    
    # Таблица временных слотов
    cursor.execute('''CREATE TABLE IF NOT EXISTS time_slots (
        slot_id INTEGER PRIMARY KEY,
        date TEXT,
        time TEXT,
        is_available BOOLEAN
    )''')
    
    # Таблица записей
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
    
    # Таблица администраторов
    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
        admin_id INTEGER PRIMARY KEY
    )''')
    
    conn.commit()
    conn.close()

# Функции для работы с БД

# Проверка администратора
def is_admin(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE admin_id = ?", (user_id,))
    return cursor.fetchone() is not None

# Добавление услуги
def add_service(service_name, service_price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (service_name, service_price) VALUES (?, ?)", (service_name, service_price))
    conn.commit()
    conn.close()

# Удаление услуги
def remove_service(service_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM services WHERE service_id = ?", (service_id,))
    conn.commit()
    conn.close()

# Получение списка услуг
def get_services():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    conn.close()
    return services

# Добавление временного слота
def add_time_slot(date, time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO time_slots (date, time, is_available) VALUES (?, ?, 1)", (date, time))
    conn.commit()
    conn.close()

# Удаление временного слота
def remove_time_slot(slot_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM time_slots WHERE slot_id = ?", (slot_id,))
    conn.commit()
    conn.close()

# Получение доступных временных слотов
def get_available_slots():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM time_slots WHERE is_available = 1")
    slots = cursor.fetchall()
    conn.close()
    return slots

# Бронирование записи
def book_appointment(user_id, service_id, slot_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (user_id, service_id, slot_id, booked_on) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", 
                   (user_id, service_id, slot_id))
    cursor.execute("UPDATE time_slots SET is_available = 0 WHERE slot_id = ?", (slot_id,))
    conn.commit()
    conn.close()

# Получение истории записей пользователя
def get_user_appointments(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE user_id = ?" , (user_id,))
    appointments = cursor.fetchall()
    conn.close()
    return appointments

# Регистрация пользователя
def register_user(user_id, username, phone):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, username, phone, registered_on) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", 
                   (user_id, username, phone))
    conn.commit()
    conn.close()

# Проверка, зарегистрирован ли пользователь
def is_registered(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, ))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def is_admin(user_id):
    admins = [5661787054]  # Список ID администраторов (замените на реальные ID)
    return user_id in admins

def cancel_booking(user_id, booking_id):
    """Отменяет запись пользователя по ID записи.

    Args:
        user_id (int): ID пользователя.
        booking_id (int): ID записи для отмены.

    Returns:
        bool: True, если отмена прошла успешно, иначе False.
    """
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Выполнение SQL-запроса для удаления записи
        cursor.execute("DELETE FROM appointments WHERE user_id = ? AND slot_id = ?", (user_id, booking_id))
        
        # Проверка, была ли запись удалена
        if cursor.rowcount > 0:
            conn.commit()  # Сохраняем изменения
            return True  # Успешно отменено
        else:
            return False  # Запись не найдена или не удалена

    except sqlite3.Error as e:
        print(f"Ошибка при отмене записи: {e}")
        return False  # В случае ошибки возвращаем False

    finally:
        # Закрываем соединение с базой данных
        if conn:
            conn.close()