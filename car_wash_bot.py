import telebot
from config import TOKEN
from user import handle_user_commands
from admin import handle_admin_commands
from database import init_db

bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных при запуске
init_db()

# Обработка команд пользователя
handle_user_commands(bot)

# Обработка команд администратора
handle_admin_commands(bot)

# Запуск бота
bot.polling()

