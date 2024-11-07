import logging
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Вставьте ваш токен здесь
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Функция для отправки сообщения
def send_daily_message(context: CallbackContext):
    chat_id = context.job.context  # Получаем chat_id из контекста задачи
    context.bot.send_message(chat_id=chat_id, text='Ваше ежедневное сообщение!')

# Команда /start для получения chat_id
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Бот запущен! Вы будете получать сообщения каждый день в 12:00.')
    
    # Запланируем задачу на каждый день в 12:00
    context.job_queue.run_daily(send_daily_message, time=time(12, 0), context=update.message.chat_id)

def main():
    # Создаем Updater и передаем ему токен бота
    updater = Updater(TOKEN)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Регистрация обработчиков команд
    dp.add_handler(CommandHandler("start", start))

    # Запускаем бота
    updater.start_polling()

    # Запускаем планировщик
    updater.idle()

if __name__ == '__main__':
    main()
