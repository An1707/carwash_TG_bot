from telebot import TeleBot
from database import is_admin, add_service, remove_service, add_time_slot

def handle_admin_commands(bot: TeleBot):
    @bot.message_handler(commands=['add_service'])
    def add_service_handler(message):
        if is_admin(message.from_user.id):
            # Логика добавления услуги
        else:
            bot.send_message(message.from_user.id, "У вас нет прав доступа.")

    @bot.message_handler(commands=['remove_service'])
    def remove_service_handler(message):
        if is_admin(message.from_user.id):
            # Логика удаления услуги
        else:
            bot.send_message(message.from_user.id, "У вас нет прав доступа.")

