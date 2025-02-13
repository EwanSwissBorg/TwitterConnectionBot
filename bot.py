from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
import tweepy
from session_store import save_session

# Charger les variables d'environnement
load_dotenv()

# Configuration Twitter OAuth
oauth1_user_handler = tweepy.OAuth1UserHandler(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET'),
    callback=os.getenv('TWITTER_CALLBACK_URL')
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Obtenir l'URL d'autorisation et le token
    auth_url = oauth1_user_handler.get_authorization_url()
    oauth_token = oauth1_user_handler.request_token["oauth_token"]
    
    # Stocker le chat_id et le request_token
    save_session(
        oauth_token, 
        update.effective_chat.id,
        oauth1_user_handler.request_token
    )
    print(f"Stored session: {oauth_token} -> {update.effective_chat.id}")
    
    keyboard = [
        [InlineKeyboardButton("Connect Twitter", url=auth_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Welcome! Please connect your Twitter account:',
        reply_markup=reply_markup
    )

def main():
    app = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()
    app.add_handler(CommandHandler('start', start))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()