import logging
from telegram import Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telethon import TelegramClient, events
from pytgcalls import PyTgCalls
from pytgcalls import filters as fl
from pytgcalls.types import Update as TgCallsUpdate
from pytgcalls.types.stream import StreamEnded
import schedule
from config import BOT_TOKEN, ADMIN_IDS, GOOD_MORNING_TIME, GOOD_NIGHT_TIME
from handlers import start, song_request, welcome_new_member, inform_left_member, greeting_response, manage_queue, download_song, add_song, remove_song, show_playlist, play, pause, resume, stop, seek, set_volume, skip
from scheduler import send_good_morning, send_good_night
from queue_backup import QueueManager
from members import MemberManager
from database import Database
import time
import asyncio
import os
import flask
from threading import Thread


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize managers
queue_manager = QueueManager()
member_manager = MemberManager()
database = Database()

# Initialize Telethon client
API_ID = 24381900
API_HASH = "b3b605e4006b1ffb1b2f8508a14103fa"
client = TelegramClient('session_name',  API_ID, API_HASH)       
app = flask.Flask('')

# Initialize PyTgCalls
call_py = PyTgCalls(client)

async def main():
    # Initialize bot application
    global application
    application = Application.builder().token('8092275297:AAHgQyldjbOMEfC-16W6Zkp1h3-z7Da3rOE').build()

async def start(update, context):
    await update.message.reply_text("Hello! I'm alive.")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

# Adding Handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Run the bot
application.run_polling()
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, song_request))
    application.add_handler(MessageHandler(filters.Regex(r'(?i)good (morning|night|evening|afternoon)'), greeting_response))
    application.add_handler(CommandHandler('managequeue', manage_queue))
    application.add_handler(CommandHandler('download', download_song))
    application.add_handler(CommandHandler('addsong', add_song))
    application.add_handler(CommandHandler('removesong', remove_song))
    application.add_handler(CommandHandler('showplaylist', show_playlist))
    application.add_handler(CommandHandler('play', play))
    application.add_handler(CommandHandler('pause', pause))
    application.add_handler(CommandHandler('resume', resume))
    application.add_handler(CommandHandler('stop', stop))
    application.add_handler(CommandHandler('seek', seek))
    application.add_handler(CommandHandler('setvolume', set_volume))
    application.add_handler(CommandHandler('skip', skip))

    # Start the bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling(stop_signals=None)
    await application.idle()

async def echo(update, context):
    print(f"Received message: {update.message.text}")  # Debugging print

    await update.message.reply_text(f"You said: {update.message.text}")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
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

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()


if __name__ == "__main__":
    # Start Telethon client
    client.start(bot_token=BOT_TOKEN)
    call_py.start()

    loop = asyncio.get_event_loop()

    # Ensure the event loop is running properly
    try:
        loop.run_until_complete(main())  # Run the bot inside the active loop
    except RuntimeError:
        # If the event loop is already running, use create_task
        loop.create_task(main())

    # Keep the bot alive
    loop.run_forever()
