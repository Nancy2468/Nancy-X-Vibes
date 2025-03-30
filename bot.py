import os from pyrogram import Client from pytgcalls import PyTgCalls import handlers  # Importing the handlers.py file

Initialize the bot

bot = Client("NancyXBot", api_id=os.getenv("API_ID"), api_hash=os.getenv("API_HASH"), bot_token=os.getenv("BOT_TOKEN"))

Initialize voice call

call = PyTgCalls(bot)

Start bot and call

bot.start() call.start()

print("NancyXBot is running!") bot.idle()

