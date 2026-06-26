import os
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def anti_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    admins = await context.bot.get_chat_administrators(
        update.effective_chat.id
    )
    admin_ids = [admin.user.id for admin in admins]

    # Admin ke messages delete nahi honge
    if update.effective_user.id in admin_ids:
        return

    # Member ne link bheja to delete karo
    if re.search(r"(https?://|www\.|t\.me/)", update.message.text.lower()):
        try:
            await update.message.delete()
            print(f"Deleted link from {update.effective_user.id}")
        except Exception as e:
            print(f"Delete error: {e}")

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not found")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            anti_link
        )
    )

    print("ParthTraderAlerts_Bot started...")
    app.run_polling(
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
