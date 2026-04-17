import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

TOKEN = "8602440281:AAFVx5FZz81YxYgEw-rinPZEZKGQeuhlbzM"


async def is_admin(update, context):
    chat = update.effective_chat
    user_id = update.effective_user.id

    member = await context.bot.get_chat_member(chat.id, user_id)
    return member.status in ("administrator", "creator")


async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    text = message.text

    if not text:
        return

    if await is_admin(update, context):
        return

    text_lower = text.lower()

    banned = [
        "сбор", "донат", "перевод", "карта",
        "qiwi", "paypal", "usdt", "btc",
        "http://", "https://", "t.me/"
    ]

    for word in banned:
        if word in text_lower:
            await message.delete()
            return

    if re.search(r"\b\d{16}\b", text) or re.search(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", text):
        await message.delete()
        return


# ❗ отдельный обработчик системных сообщений
async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except:
        pass


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # текстовые сообщения
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    # вход/выход участников
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER,
        delete_service_messages
    ))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()