# Twitter Authentication Telegram Bot

## Quick Start

1. Install required packages:
pip install python-telegram-bot python-dotenv tweepy flask

2. Create a `.env` file with:
BOT_TOKEN=your_telegram_bot_token
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_CALLBACK_URL=your_ngrok_url

3. Start ngrok:
ngrok http 8000

4. Update TWITTER_CALLBACK_URL in .env with your ngrok URL

5. Start the server:
python3 server.py

6. In a new terminal, start the bot:
python3 bot.py

7. Go to your Telegram bot and type /start