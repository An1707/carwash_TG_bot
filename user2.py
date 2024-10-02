from telebot import TeleBot, types
from database import is_registered, register_user, get_services, get_available_slots, book_appointment, get_user_appointments, cancel_booking  # Импорт необходимых функций из модуля базы данных

def start_command(message, bot):
    """Обрабатывает команду /start."""
    bot.send_message(message.chat.id, "Добро пожаловать! Пожалуйста, зарегистрируйтесь.")
    # Логика регистрации пользователя...

def book_service(message, bot):
    """Запуск процесса записи на услугу."""
    services = get_services()
    response = "Выберите услугу:\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for service in services:
        response += f"{service[0]}. {service[1]} - {service[2]} рублей\n"
        markup.add(types.KeyboardButton(f"{service[0]} - {service[1]}"))

    markup.add(types.KeyboardButton("Отмена действия"))
    bot.send_message(message.chat.id, response + "\nВыберите:", reply_markup=markup)

    bot.register_next_step_handler(message, select_time)

def select_time(message, bot):
    """Выбор времени записи."""
    service_id = message.text.split(" - ")[0]  # Получаем ID услуги
    available_slots = get_available_slots()  # Получаем доступные слоты
    response = "Выберите время для записи:\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for slot in available_slots:
        response += f"{slot}\n"
        markup.add(types.KeyboardButton(slot))

    markup.add(types.KeyboardButton("Отмена действия"))
    bot.send_message(message.chat.id, response + "\nВыберите:", reply_markup=markup)

    bot.register_next_step_handler(message, confirm_booking, service_id)

def confirm_booking(message, service_id, bot):
    """Подтверждение записи."""
    if message.text == "Отмена действия":
        bot.send_message(message.chat.id, "Запись отменена. Вернуться в главное меню.")
        return

    appointment_time = message.text
    user_id = message.from_user.id  # Получаем ID пользователя
    book_appointment(user_id, service_id, appointment_time)  # Записываем пользователя
    bot.send_message(message.chat.id, f"Вы успешно записаны на услугу в {appointment_time}.")

def cancel_user_booking(message, bot):
    appointments = get_user_appointments(message.from_user.id)  # Получаем записи пользователя
    if not appointments:
        bot.send_message(message.chat.id, "У вас нет записей для отмены.")
        return

    response = "Выберите запись для отмены:\n"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for appointment in appointments:
        response += f"Запись №{appointment[0]}: Услуга ID {appointment[1]} в {appointment[2]}\n"
        markup.add(types.KeyboardButton(f"Отменить запись №{appointment[0]}"))

    markup.add(types.KeyboardButton("Отмена действия"))  # Кнопка для отмены
    bot.send_message(message.chat.id, response + "\nВыберите:", reply_markup=markup)
    
    bot.register_next_step_handler(message, process_cancellation)  # Ожидаем следующий шаг

def process_cancellation(message, bot):
    if message.text == "Отмена действия":
        bot.send_message(message.chat.id, "Отмена действия. Вернуться в главное меню.")
        return

    try:
        booking_id = int(message.text.split("№")[1])  # Извлекаем ID записи
        result = cancel_booking(message.from_user.id, booking_id)  # Отмена записи в базе данных
        if result:
            bot.send_message(message.chat.id, "Запись успешно отменена!")
        else:
            bot.send_message(message.chat.id, "Ошибка отмены записи. Попробуйте еще раз.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, попробуйте еще раз.")
