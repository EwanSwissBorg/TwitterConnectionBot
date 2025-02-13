from flask import Flask, request
from telegram import Bot
import asyncio
import os
from dotenv import load_dotenv
import tweepy
from session_store import get_session

load_dotenv()

app = Flask(__name__)
bot = Bot(token=os.getenv('BOT_TOKEN'))

# Configuration Twitter OAuth
oauth1_user_handler = tweepy.OAuth1UserHandler(
    os.getenv('TWITTER_API_KEY'),
    os.getenv('TWITTER_API_SECRET'),
    callback=os.getenv('TWITTER_CALLBACK_URL')
)

async def send_telegram_message(chat_id, message):
    await bot.send_message(chat_id=chat_id, text=message)

@app.route('/', methods=['GET'])
def twitter_callback():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    
    print(f"Received callback with token: {oauth_token}")
    
    session = get_session(oauth_token)
    if session:
        chat_id = session['chat_id']
        try:
            # Restaurer le request_token
            oauth1_user_handler.request_token = session['request_token']
            
            # Obtenir l'accès Twitter
            access_token, access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
            
            # Créer un client Twitter
            client = tweepy.Client(
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            
            # Obtenir les informations de l'utilisateur
            user = client.get_me()
            message = f"Twitter connection successful! Welcome @{user.data.username}"
            
            # Envoyer le message Telegram
            asyncio.run(send_telegram_message(chat_id, message))
            print(f"Message sent to chat_id: {chat_id}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            asyncio.run(send_telegram_message(chat_id, f"An error occurred during Twitter connection: {str(e)}"))
    else:
        print(f"No session found for token: {oauth_token}")
    
    return "You can close this window and go back to Telegram!"

if __name__ == '__main__':
    app.run(port=8000, debug=True)