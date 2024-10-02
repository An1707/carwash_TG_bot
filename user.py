# user.py
from telebot import TeleBot, types
from database import is_registered, register_user, get_services, get_available_slots, book_appointment, get_user_appointments, cancel_booking

def handle_user_commands(bot: TeleBot):
    # Главное меню с кнопками "Начать" и "История"
    def show_main_menu(chat_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_btn = types.KeyboardButton("Начать")
        book_btn = types.KeyboardButton("Запись")
        history_btn = types.KeyboardButton("История")
        cancel_book_btn = types.KeyboardButton("Отмена записи")
        markup.add(start_btn, history_btn, book_btn, cancel_book_btn)
        bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

    # Команда /start - регистрация пользователя
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id
        if not is_registered(user_id):
            bot.send_message(user_id, "Добро пожаловать! Пожалуйста, зарегистрируйтесь. Введите ваше имя:")
            bot.register_next_step_handler(message, get_name)
        else:
            bot.send_message(user_id, "Вы уже зарегистрированы!")
            show_main_menu(user_id)

    def get_name(message):
        username = message.text
        bot.send_message(message.from_user.id, "Введите ваш номер телефона:")
        bot.register_next_step_handler(message, lambda m: complete_registration(m, username))

    def complete_registration(message, username):
        phone = message.text
        register_user(message.from_user.id, username, phone)
        bot.send_message(message.from_user.id, "Вы успешно зарегистрированы!")
        show_main_menu(message.from_user.id)

    # Обработка нажатий на кнопки "Начать" и "История"
    @bot.message_handler(func=lambda message: message.text in ["Начать", "Запись", "История", "Отмена действия", "Отмена записи"])
    def handle_buttons(message):
        if message.text == "Запись":
            show_services(message)
        elif message.text == "История":
            show_history(message)
        elif message.text == "Отмена действия":
            show_main_menu(message.chat.id)
        elif message.text == "Отмена записи":
            cancel_user_booking(message)
        

    # Показываем услуги в виде кнопок
    def show_services(message):
        services = get_services()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for service in services:
            markup.add(types.KeyboardButton(f"{service[0]}. {service[1]} - {service[2]} руб."))
        markup.add(types.KeyboardButton("Отмена действия"))  # Кнопка отмены
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=markup)
        bot.register_next_step_handler(message, select_service)

    # После выбора услуги показываем доступные временные слоты
    def select_service(message):
        if message.text == "Отмена действия":
            show_main_menu(message.chat.id)
            return
        
        service_id = int(message.text.split('.')[0])
        slots = get_available_slots()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for slot in slots:
            markup.add(types.KeyboardButton(f"{slot[0]}. {slot[1]} {slot[2]}"))
        markup.add(types.KeyboardButton("Отмена действия"))  # Кнопка отмены
        bot.send_message(message.chat.id, "Выберите время:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: confirm_booking(m, service_id))

    # Подтверждение записи
    def confirm_booking(message, service_id):
        if message.text == "Отмена действия":
            show_main_menu(message.chat.id)
            return
        
        slot_id = int(message.text.split('.')[0])
        book_appointment(message.from_user.id, service_id, slot_id)
        bot.send_message(message.chat.id, "Ваша запись подтверждена!")
        show_main_menu(message.chat.id)

    # История записей
    def show_history(message):
        appointments = get_user_appointments(message.from_user.id)
        response = "Ваши записи:\n"
        if not appointments:
            response = "У вас нет записей."
        else:
            for appointment in appointments:
                response += f"Запись №{appointment[0]} на услугу {appointment[1]}\n"
        bot.send_message(message.chat.id, response)
        show_main_menu(message.chat.id)

    # Метод для отмены записи
    def cancel_user_booking(message):
        appointments = get_user_appointments(message.from_user.id)
        if not appointments:
            bot.send_message(message.chat.id, "У вас нет записей для отмены.")
            show_main_menu(message.chat.id)
            return

        response = "Выберите запись для отмены:\n"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for appointment in appointments:
            response += f"Запись №{appointment[0]}: {appointment[1]} в {appointment[2]}\n"
            markup.add(types.KeyboardButton(f"Отменить запись №{appointment[0]}"))

        markup.add(types.KeyboardButton("Отмена действия"))  # Кнопка отмены
        bot.send_message(message.chat.id, response + "\nВыберите:", reply_markup=markup)
        bot.register_next_step_handler(message, process_cancellation)

    def process_cancellation(message):
        if message.text == "Отмена действия":
            show_main_menu(message.chat.id)
            return

        booking_id = int(message.text.split("№")[1])
        result = cancel_booking(message.from_user.id, booking_id)  # Метод для отмены записи
        if result:
            bot.send_message(message.chat.id, "Запись успешно отменена!")
        else:
            bot.send_message(message.chat.id, "Ошибка отмены записи. Попробуйте еще раз.")
        show_main_menu(message.chat.id)