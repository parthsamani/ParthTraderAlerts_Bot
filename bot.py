from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
import re

TOKEN = os.environ["BOT_TOKEN"]

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in admins]

    # Admin/Owner ko allow karo
    if user_id in admin_ids:
        return

    text = update.message.text.lower()

    # Link detect karo
    if re.search(r"(https?://|www\.|t\.me/)", text):
        try:
            await update.message.delete()
        except Exception as e:
            print(e)

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, anti_link)
)

app.run_polling()
