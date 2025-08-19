from aiogram import Bot
from aiogram.types import Message
import yookassa
from yookassa import Payment
import uuid
from config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

yookassa.Configuration.account_id = YOOKASSA_SHOP_ID
yookassa.Configuration.secret_key = YOOKASSA_SECRET_KEY

bot_instance = None

def set_bot(bot: Bot):
    global bot_instance
    bot_instance = bot
    logger.info("✅ Бот передан в модуль оплаты")

async def create_invoice(message: Message):
    global bot_instance

    logger.info(f"Создание счёта для пользователя {message.from_user.id}")

    try:
        payment = Payment.create({
            "amount": {
                "value": "199.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/HabitlyTrackerBot"
            },
            "capture": True,
            "description": "Подписка на ИИ-анализ привычек"
        }, uuid.uuid4())

        confirmation_url = payment.confirmation.confirmation_url
        await message.answer(
            "💳 Оплати подписку:\n"
            f"[Перейти к оплате]({confirmation_url})",
            parse_mode="Markdown"
        )

        await asyncio.sleep(600)  # Проверка через 10 минут

        updated = Payment.find_one(payment.id)
        logger.info(f"Платёж ID: {payment.id}, Статус: {updated.status}, Оплачено: {updated.paid}")

        if updated.paid:
            user_id = message.from_user.id
            from db import get_db
            conn = get_db()
            cur = conn.cursor()
            from datetime import datetime, timedelta
            new_date = (datetime.now().date() + timedelta(days=30)).isoformat()
            cur.execute("UPDATE users SET premium_until = ?, trial_used = 1 WHERE id = ?", (new_date, user_id))
            conn.commit()
            conn.close()

            logger.info(f"✅ Подписка активирована для пользователя {user_id} до {new_date}")

            if bot_instance:
                try:
                    await bot_instance.send_message(user_id, "✅ Подписка активирована! Доступ к ИИ-отчётам открыт.")
                except Exception as e:
                    logger.error(f"Не удалось отправить сообщение: {e}")
    except Exception as e:
        logger.error(f"🔴 Ошибка при создании счёта: {e}")
        await message.answer(f"Ошибка оплаты: {str(e)}")