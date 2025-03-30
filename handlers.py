import os import time import sqlite3 import threading import youtube_dl from pyrogram import Client, filters from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message from pytgcalls import PyTgCalls from pytgcalls.types.input_stream import AudioPiped import openai
Initialize bot & voice call

bot = Client("NancyXBot") call = PyTgCalls(bot)

Database setup

conn = sqlite3.connect("music_bot.db", check_same_thread=False) cursor = conn.cursor() cursor.execute(""" CREATE TABLE IF NOT EXISTS playlists ( chat_id INTEGER, name TEXT, song TEXT, PRIMARY KEY (chat_id, name, song) ) """) conn.commit()

Queues per group

queues = {}

Function to delete expired buttons

def delete_inline_buttons(message: Message): time.sleep(180) message.edit_text("⏳ Inline options expired!")

Function to play music

def play_music(chat_id, url): if chat_id not in queues: queues[chat_id] = [] queues[chat_id].append(url) if len(queues[chat_id]) == 1: call.join_group_call(chat_id, AudioPiped(url))

/start command

@bot.on_message(filters.command("start")) def start_command(client, message: Message): if message.chat.type == "private": buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("🎵 Explore Music", callback_data="explore_music")], [InlineKeyboardButton("ℹ Help", callback_data="help_menu")] ]) sent_message = message.reply_photo("start_image.jpg", caption="Welcome to Nancy X Vibes! 🎶", reply_markup=buttons) else: sent_message = message.reply_photo("bot_dp.jpg", caption="Hello! Use /help for commands.") threading.Thread(target=delete_inline_buttons, args=(sent_message,)).start()

/play command

@bot.on_message(filters.command("play")) def play_song(client, message: Message): chat_id = message.chat.id query = " ".join(message.command[1:]) if not query: message.reply_text("Please provide a song name or URL!") return ydl_opts = {'format': 'bestaudio', 'outtmpl': f'./downloads/{chat_id}.mp3'} with youtube_dl.YoutubeDL(ydl_opts) as ydl: info = ydl.extract_info(query, download=True) url = ydl.prepare_filename(info) play_music(chat_id, url) message.reply_text(f"🎵 Playing: {info['title']}")

/stop command

@bot.on_message(filters.command("stop")) def stop_song(client, message: Message): chat_id = message.chat.id call.leave_group_call(chat_id) queues[chat_id] = [] message.reply_text("⏹ Music stopped!")

/skip command

@bot.on_message(filters.command("skip")) def skip_song(client, message: Message): chat_id = message.chat.id if chat_id in queues and len(queues[chat_id]) > 1: queues[chat_id].pop(0) next_song = queues[chat_id][0] call.change_stream(chat_id, AudioPiped(next_song)) message.reply_text("⏭ Skipping song!") else: call.leave_group_call(chat_id) queues[chat_id] = [] message.reply_text("✅ Queue finished, leaving call!")

Playlist management

@bot.on_message(filters.command("addplaylist")) def add_playlist(client, message: Message): chat_id = message.chat.id name = " ".join(message.command[1:]) if not name: message.reply_text("Please provide a playlist name!") return cursor.execute("INSERT OR IGNORE INTO playlists (chat_id, name, song) VALUES (?, ?, ?)", (chat_id, name, "")) conn.commit() message.reply_text(f"Playlist '{name}' created!")

@bot.on_message(filters.command("playlist")) def show_playlists(client, message: Message): chat_id = message.chat.id cursor.execute("SELECT DISTINCT name FROM playlists WHERE chat_id = ?", (chat_id,)) playlists = cursor.fetchall() if not playlists: message.reply_text("No playlists available!") return buttons = [[InlineKeyboardButton(name[0], callback_data=f"playlist_{name[0]}")] for name in playlists] sent_message = message.reply_text("🎶 Playlists:", reply_markup=InlineKeyboardMarkup(buttons)) threading.Thread(target=delete_inline_buttons, args=(sent_message,)).start()

/Nancy (ChatGPT integration)

@bot.on_message(filters.regex(r'^/Nancy (.+)')) def ask_chatgpt(client, message: Message): query = message.matches[0].group(1) response = openai.ChatCompletion.create( model="gpt-4", messages=[{"role": "user", "content": query}] ) answer = response['choices'][0]['message']['content'] message.reply_text(f"🔮 {answer}")

Auto-pause if no users in VC for 5 minutes

def auto_pause(): while True: time.sleep(300) for chat_id in list(queues.keys()): if bot.get_chat_members_count(chat_id) <= 1: call.leave_group_call(chat_id) queues.pop(chat_id, None) bot.send_message(chat_id, "⏸ No users in VC, music paused!") threading.Thread(target=auto_pause, daemon=True).start()

Scheduled messages

def send_scheduled_messages(): while True: current_time = time.strftime("%H:%M") if current_time == "07:00": bot.send_message("@your_group", "☀ Good Morning! Have a great day ahead!") elif current_time == "22:00": bot.send_message("@your_group", "🌙 Good Night! Sweet dreams!") time.sleep(60) threading.Thread(target=send_scheduled_messages, daemon=True).start()

Start bot

bot.start() call.start() print("NancyXBot is running!") bot.idle()

