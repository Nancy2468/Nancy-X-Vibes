from telegram import Update, Bot
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from config import ADMIN_IDS, START_ANIMATION
from queue_backup import QueueManager
from members import MemberManager
from database import Database
import yt_dlp

queue_manager = QueueManager()
member_manager = MemberManager()
database = Database()

def start(update: Update, context: CallbackContext):
    update.message.reply_animation(animation=open(START_ANIMATION, 'rb'), caption="🎶 Welcome to Nancy Bot! 🎶\n\nEnjoy the music experience!")
    update.message.reply_text('Welcome to the Telegram Music Bot!')

def song_request(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    song = update.message.text
    queue_manager.add_to_queue(group_id, song)
    update.message.reply_text(f'Song "{song}" added to the queue!')
    queue_manager.update_activity(group_id)

async def welcome_new_member(event):
    chat = await event.get_chat()
    new_user = await event.get_user()
    member_manager.add_member(new_user.id, new_user.first_name)
    await event.reply(f'Welcome, {new_user.first_name}!\nID: {new_user.id}\nDate of Birth: {new_user.date_of_birth or "N/A"}')

async def inform_left_member(event):
    chat = await event.get_chat()
    left_user = await event.get_user()
    member_info = member_manager.get_member_info(left_user.id)
    member_manager.remove_member(left_user.id)
    if member_info:
        name, date_of_birth = member_info
        await event.reply(f'{name} (ID: {left_user.id}) has left the chat.\nDate of Birth: {date_of_birth or "N/A"}')
    else:
        await event.reply(f'{left_user.first_name} (ID: {left_user.id}) has left the chat.')

def greeting_response(update: Update, context: CallbackContext):
    user = update.message.from_user
    if user.id in ADMIN_IDS:
        greeting = update.message.text.lower()
        update.message.reply_text(f'{greeting.capitalize()}, {user.first_name}!')

def manage_queue(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        group_id = update.message.chat_id
        command = context.args[0]
        if command == 'change':
            old_index = int(context.args[1])
            new_index = int(context.args[2])
            queue_manager.change_song_position(group_id, old_index, new_index)
            update.message.reply_text('Queue updated!')
        elif command == 'remove':
            index = int(context.args[1])
            queue_manager.remove_from_queue(group_id, index)
            update.message.reply_text('Song removed from queue!')

def download_song(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        url = context.args[0]
        format = context.args[1]
        ydl_opts = {
            'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio',
            'outtmpl': f'Nancy Bot-%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3' if format == 'mp3' else 'mp4',
                'preferredquality': '192',
            }] if format == 'mp3' else []
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        update.message.reply_text('Song downloaded!')

def add_song(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        group_id = update.message.chat_id
        song = ' '.join(context.args)
        database.add_song(group_id, song)
        update.message.reply_text(f'Song "{song}" added to the playlist!')

def remove_song(update: Update, context: CallbackContext):
    if update.message.from_user.id in ADMIN_IDS:
        group_id = update.message.chat_id
        song_id = int(context.args[0])
        database.remove_song(group_id, song_id)
        update.message.reply_text(f'Song with ID {song_id} removed from the playlist!')

def show_playlist(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    playlist = database.get_playlist(group_id)
    if playlist:
        message = "Playlist:\n" + "\n".join([f"{song_id}: {song}" for song_id, song in playlist])
    else:
        message = "The playlist is empty."
    update.message.reply_text(message)

def play(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    queue_manager.play(group_id)

def pause(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    queue_manager.pause(group_id)

def resume(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    queue_manager.resume(group_id)

def stop(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    queue_manager.stop(group_id)

def seek(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    seconds = int(context.args[0])
    queue_manager.seek(group_id, seconds)

def set_volume(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    volume = int(context.args[0])
    queue_manager.set_volume(group_id, volume)

def skip(update: Update, context: CallbackContext):
    group_id = update.message.chat_id
    queue_manager.play_next(group_id)
