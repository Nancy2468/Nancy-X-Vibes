from pyrogram import Client, filters from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message from pytgcalls import PyTgCalls from pytgcalls.types.input_stream import AudioPiped import youtube_dl import os import threading import time

Initialize bot and PyTgCalls

bot = Client("NancyXBot") call = PyTgCalls(bot)

Dictionary to store playlists per group

playlists = {} queues = {}

Function to play music in voice chat

def play_music(chat_id, url): if chat_id not in queues: queues[chat_id] = [] queues[chat_id].append(url) if len(queues[chat_id]) == 1:  # If first song, start playing call.join_group_call(chat_id, AudioPiped(url))

Function to delete inline buttons after 3 minutes

def delete_inline_buttons(message: Message): time.sleep(180) message.edit_text("⏳ Inline options expired!")

Command: /start

@bot.on_message(filters.command("start")) def start_command(client, message: Message): if message.chat.type == "private": buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("🎵 Explore Music", callback_data="explore_music")], [InlineKeyboardButton("ℹ Help", callback_data="help_menu")] ]) sent_message = message.reply_photo("start_image.jpg", caption="Welcome to Nancy X Vibes! 🎶\n\nEnjoy unlimited music with a futuristic touch!", reply_markup=buttons) else: sent_message = message.reply_photo("bot_dp.jpg", caption="Hello! I'm Nancy X Vibes. Use /help to see available commands.") threading.Thread(target=delete_inline_buttons, args=(sent_message,)).start()

Command: /play <song_name or URL>

@bot.on_message(filters.command("play")) def play_song(client, message: Message): chat_id = message.chat.id query = " ".join(message.command[1:]) if not query: message.reply_text("Please provide a song name or URL!") return

# Download audio from YouTube
ydl_opts = {'format': 'bestaudio', 'outtmpl': f'./downloads/{chat_id}.mp3'}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(query, download=True)
    url = ydl.prepare_filename(info)
    
play_music(chat_id, url)
message.reply_text(f"🎵 Playing: {info['title']}")

Command: /stop

@bot.on_message(filters.command("stop")) def stop_song(client, message: Message): chat_id = message.chat.id call.leave_group_call(chat_id) queues[chat_id] = [] message.reply_text("⏹ Music stopped!")

Command: /skip

@bot.on_message(filters.command("skip")) def skip_song(client, message: Message): chat_id = message.chat.id if chat_id in queues and len(queues[chat_id]) > 1: queues[chat_id].pop(0) next_song = queues[chat_id][0] call.change_stream(chat_id, AudioPiped(next_song)) message.reply_text("⏭ Skipping song!") else: call.leave_group_call(chat_id) queues[chat_id] = [] message.reply_text("✅ Queue finished, leaving call!")

Playlist Management Commands

@bot.on_message(filters.command("addplaylist")) def add_playlist(client, message: Message): chat_id = message.chat.id name = " ".join(message.command[1:]) if not name: message.reply_text("Please provide a playlist name!") return if chat_id not in playlists: playlists[chat_id] = {} playlists[chat_id][name] = [] message.reply_text(f"Playlist '{name}' created!")

@bot.on_message(filters.command("playlist")) def show_playlists(client, message: Message): chat_id = message.chat.id if chat_id not in playlists or not playlists[chat_id]: message.reply_text("No playlists available!") return buttons = [[InlineKeyboardButton(name, callback_data=f"playlist_{name}")] for name in playlists[chat_id]] sent_message = message.reply_text("🎶 Playlists:", reply_markup=InlineKeyboardMarkup(buttons)) threading.Thread(target=delete_inline_buttons, args=(sent_message,)).start()

Command: /help

@bot.on_message(filters.command("help")) def send_help(client, message: Message): buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("🎶 Music Commands", callback_data="music_help")], [InlineKeyboardButton("🔧 Admin Commands", callback_data="admin_help")] ]) sent_message = message.reply_text("Here are my commands! Click the buttons below for more info.", reply_markup=buttons) threading.Thread(target=delete_inline_buttons, args=(sent_message,)).start()

Command: /Nancy <question>

@bot.on_message(filters.regex(r'^/Nancy (.+)')) def ask_chatgpt(client, message: Message): query = message.matches[0].group(1) response = f"🔮 Searching for: {query}\nAnswer: ChatGPT response here..." message.reply_text(response)

Start bot and PyTgCalls

bot.start() call.start()

print("NancyXBot is running!") bot.idle()

