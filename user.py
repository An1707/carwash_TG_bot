from telebot import TeleBot
from database import get_services, register_user, book_appointment

def handle_user_commands(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id
        # Логика регистрации и обработки пользователей

    @bot.message_handler(commands=['book'])
    def book_service(message):
        # Логика записи пользователя на услугу

