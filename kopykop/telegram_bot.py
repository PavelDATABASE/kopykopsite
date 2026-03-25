import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from django.conf import settings

# Токен вашего бота
TELEGRAM_BOT_TOKEN = '8600160789:AAFEflOaM-iMaWnaj_spKRruB437jFSfXIo'

# ID чата администратора
ADMIN_CHAT_ID = '783113839'


async def send_order_notification(order):
    """Отправляет уведомление администратору о новом заказе"""
    print(f"Попытка отправить уведомление для заказа {order.orders_name}")
    print(f"Токен: {TELEGRAM_BOT_TOKEN}")
    print(f"Chat ID: {ADMIN_CHAT_ID}")
    
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    message = f"🆕 <b>Новый заказ!</b>\n\n"
    message += f"📋 <b>Заказ:</b> {order.orders_name}\n"
    message += f"📝 <b>Услуга:</b> {order.name.name}\n"
    message += f"👤 <b>ФИО:</b> {order.fio}\n"
    message += f"📞 <b>Телефон:</b> {order.number}\n"
    message += f"📝 <b>Доп. информация:</b> {order.description}\n"
    message += f"🆔 <b>ID заказа:</b> {order.id}"
    
    try:
        # Сначала отправляем текст сообщения
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
        
        # Если есть файл, отправляем его
        if order.file:
            # Получаем полный путь к файлу
            file_path = order.file.path
            
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    await bot.send_document(
                        chat_id=ADMIN_CHAT_ID,
                        document=f,
                        caption=f"📎 <b>Файл к заказу:</b> {order.orders_name}",
                        parse_mode='HTML'
                    )
                print(f"📎 Файл отправлен: {file_path}")
            else:
                print(f"⚠️ Файл не найден: {file_path}")
        
        print(f"✅ Уведомление о заказе {order.orders_name} отправлено")
    except TelegramError as e:
        print(f"❌ Ошибка отправки Telegram-сообщения: {e}")


def notify_admin(order):
    """Синхронная обёртка для вызова асинхронной функции"""
    try:
        asyncio.run(send_order_notification(order))
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")
