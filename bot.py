from pyrogram import Client
from pytgcalls import PyTgCalls
import logging

# Bot API details (Replace with your API details)
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Initialize bot
bot = Client(
    "NancyXBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="handlers")  # Loads commands from handlers.py
)

# Initialize PyTgCalls for voice chat
call = PyTgCalls(bot)

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Start bot
async def start_bot():
    await bot.start()
    await call.start()
    print("✅ Nancy X Vibes Bot is now running!")
    await bot.send_message("me", "🚀 **Bot Started Successfully!**")

# Run bot
if __name__ == "__main__":
    bot.run()
