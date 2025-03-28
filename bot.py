import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from telethon.sync import TelegramClient
from telethon import TelegramClient, events
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from pytgcalls.types import Update as TgCallsUpdate
from pytgcalls.types.stream import StreamEnded
import schedule
from config import BOT_TOKEN, ADMIN_IDS, GOOD_MORNING_TIME, GOOD_NIGHT_TIME
from handlers import start, play_song, pause_song, resume_song, skip_song, show_queue, add_playlist, add_song_to_playlist, remove_song_from_playlist, delete_playlist, help_command, enable_feature, disable_feature, view_playlist, song_playtime

from telegram.ext import CommandHandler
from scheduler import send_good_morning, send_good_night
from queue_backup import QueueManager
from members import MemberManager
from database import Database
import time
import asyncio
import os
from threading import Thread
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext, filters
from telegram import Bot, Update
import yt_dlp

bot = Bot(token="8092275297:AAHgQyldjbOMEfC-16W6Zkp1h3-z7Da3rOE")


# Logging setup
logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)

# Initialize managers
queue_manager = QueueManager()
member_manager = MemberManager()
database = Database()

# Initialize Telethon client
API_ID = 24381900
API_HASH = "b3b605e4006b1ffb1b2f8508a14103fa"
# Initialize Telegram Client
client = TelegramClient("bot_session", API_ID, API_HASH)

# Initialize Telegram Client
client = TelegramClient("bot_session", API_ID, API_HASH)

# Initialize PyTgCalls
call_py = PyTgCalls(Client)

async def start_pytgcalls():
    await client.start(bot_token=BOT_TOKEN)
    await call_py.start()
    print("✅ PyTgCalls Started Successfully")

async def send_message(update: Update, message: str):
    if message:
        await update.message.reply_text(message[:4000])  # ✅ Fixed the async function
    else:
        await update.message.reply_text("⚠️ No text provided.")  # ✅ Fixed indentation

app = Application.builder().token(BOT_TOKEN).build()

# Register command handler
app.add_handler(CommandHandler("start", send_message))



app = Application.builder().token('8092275297:AAHgQyldjbOMEfC-16W6Zkp1h3-z7Da3rOE').build()

async def start(update, context):
    await update.message.reply_text("Hello! I'm alive.")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

# Adding Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Basic Commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("play", play_song))
app.add_handler(CommandHandler("pause", pause_song))
app.add_handler(CommandHandler("resume", resume_song))
app.add_handler(CommandHandler("skip", skip_song))
app.add_handler(CommandHandler("queue", show_queue))

# Admin Commands
app.add_handler(CommandHandler("addplaylist", add_playlist))
app.add_handler(CommandHandler("addsong", add_song_to_playlist))
app.add_handler(CommandHandler("removesong", remove_song_from_playlist))
app.add_handler(CommandHandler("deleteplaylist", delete_playlist))
app.add_handler(CommandHandler("enable", enable_feature))
app.add_handler(CommandHandler("disable", disable_feature))










@client.on(events.ChatAction)
async def handler(event):
    if event.user_added:
        await welcome_new_member(event)
    elif event.user_left:
        await inform_left_member(event)

@call_py.on_update(fl.stream_end())
async def stream_end_handler(_: PyTgCalls, update: StreamEnded):
    print(f"Received update: {update}")
    if isinstance(update, StreamEnded) and update is not None:
        await queue_manager.play_next(update.chat_id)
    else:
        print("Received None for update in stream_end_handler")

if __name__ == "__main__":
    async def main():
        await start_pytgcalls()
        await app.initialize()
        await app.start()
        print("Bot is running...")  
        await app.stop()  
    app.run_polling()  # Start polling updates

    try:
        loop = asyncio.get_running_loop()
        loop.create_task(main())  # Use existing loop if running
    except RuntimeError:
        asyncio.run(main())  # Create a new loop if needed