from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
import re

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text
    if not text:
        return

    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    admin_ids = [a.user.id for a in admins]

    if update.effective_user.id in admin_ids:
        return

    if re.search(r"(https?://|www\\.|t\\.me/)", text.lower()):
        try:
            await update.message.delete()
        except:
            pass

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        delete_links
    )
)

app.run_polling()
