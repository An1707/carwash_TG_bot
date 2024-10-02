# admin.py
from telebot import TeleBot
from database import is_admin, add_service, remove_service, add_time_slot, remove_time_slot, get_services, get_available_slots

def handle_admin_commands(bot: TeleBot):
    # Команда /add_service - добавление новой услуги
    @bot.message_handler(commands=['add_service'])
    def add_service_handler(message):
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id, "Введите название новой услуги:")
            bot.register_next_step_handler(message, get_service_name)
        else:
            bot.send_message(message.from_user.id, "У вас нет прав доступа.")
    
    def get_service_name(message):
        service_name = message.text
        bot.send_message(message.from_user.id, "Введите цену услуги:")
        bot.register_next_step_handler(message, lambda m: complete_service_adding(m, service_name))
    
    def complete_service_adding(message, service_name):
        service_price = float(message.text)
        add_service(service_name, service_price)
        bot.send_message(message.from_user.id, f"Услуга '{service_name}' добавлена.")

    # Команда /remove_service - удаление услуги
    @bot.message_handler(commands=['remove_service'])
    def remove_service_handler(message):
        if is_admin(message.from_user.id):
            services = get_services()
            response = "Выберите услугу для удаления, отправив номер:\n"
            for service in services:
                response += f"{service[0]}. {service[1]}\n"
            bot.send_message(message.from_user.id, response)
            bot.register_next_step_handler(message, complete_service_removing)
        else:
            bot.send_message(message.from_user.id, "У вас нет прав доступа.")
    
    def complete_service_removing(message):
        service_id = int(message.text)
        remove_service(service_id)
        bot.send_message(message.from_user.id, "Услуга удалена.")

    # Команда /add_time_slot - добавление нового временного слота
    @bot.message_handler(commands=['add_time_slot'])
    def add_time_slot_handler(message):
        if is_admin(message.from_user.id):
            bot.send_message(message.from_user.id, "Введите дату в формате YYYY-MM-DD:")
            bot.register_next_step_handler(message, get_time_slot_date)
        else:
            bot.send_message(message.from_user.id, "У вас нет прав доступа.")
    
    def get_time_slot_date(message):
        date = message.text
        bot.send_message(message.from_user.id, "Введите время в формате HH:MM:")
        bot.register_next_step_handler(message, lambda m: complete_time_slot_adding(m, date))
    
    def complete_time_slot_adding(message, date):
        time = message.text
        add_time_slot(date, time)
        bot.send_message(message.from_user.id, f"Слот на {date} {time} добавлен.")

    # Команда /remove_time_slot - удаление временного слота
    @bot.message_handler(commands=['remove_time_slot'])
    def remove_time_slot_handler(message):
        if is_admin(message.from_user.id):
            slots = get_available_slots()
            response = "Выберите слот для удаления, отправив номер:\n"
            for slot in slots:
                response += f"{slot[0]}. {slot[1]} {slot[2]}\n"
            bot.send_message(message.from_user.id, response)
            bot.register_next_step_handler(message, complete_time_slot_removing)
        else:
            bot.send_message(message.from_user.id, "У вас нет прав доступа.")
    
    def complete_time_slot_removing(message):
        slot_id = int(message.text)
        remove_time_slot(slot_id)
        bot.send_message(message.from_user.id, "Слот удален.")

