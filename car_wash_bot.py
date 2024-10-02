# car_wash_bot.py
import telebot
from config import TOKEN
from user import handle_user_commands
from admin import handle_admin_commands
from database import init_db

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных
init_db()

# Подключение команд пользователя
handle_user_commands(bot)

# Подключение команд администратора
handle_admin_commands(bot)

# Запуск бота
bot.polling()
