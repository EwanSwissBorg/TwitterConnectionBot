from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'hello {update.effective_user.first_name}')

def main():
    app = ApplicationBuilder().token(os.getenv('TELEGRAM_BOT_TOKEN')).build()
    
    app.add_handler(CommandHandler('start', start))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()