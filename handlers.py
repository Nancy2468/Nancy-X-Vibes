from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from youtube_search import YoutubeSearch
import yt_dlp
import os
from telegram import Update
from telegram.ext import Application, CallbackContext
from pytgcalls.types import Update as TgCallsUpdate
from pytgcalls.types.stream import StreamEnded

app = Application.builder().token('8092275297:AAHgQyldjbOMEfC-16W6Zkp1h3-z7Da3rOE').build()
# Dictionary for queue management
queue = {}
playlists = {}
current_song = {}  # Stores current playing song details

### START COMMAND ###
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("💖 **Nancy X Vibes is Alive!** 💖\n\n"
                                    "🎵 I can play and manage music in your group! 🎶\n"
                                    "Type /help to see all my commands! 💡")

### PLAY COMMAND ###
async def play_song(update: Update, context: CallbackContext):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("⚠️ **Please provide a song name or YouTube link!**")
        return

    await update.message.reply_text("🔍 **Searching for song... Please wait!**")
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        video_url = f"https://www.youtube.com{results[0]['url_suffix']}"

        ydl_opts = {"format": "bestaudio/best", "quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info["url"]

        chat_id = update.message.chat_id
        queue.setdefault(chat_id, []).append((audio_url, results[0]["title"]))

        if len(queue[chat_id]) > 1:
            await update.message.reply_text(f"🎵 **Added to queue:** {results[0]['title']}")
        else:
                await call_py.join_group_call(chat_id, StreamEnded(audio_url))
                await update.message.reply_text(f"🎶 **Now Playing:** {results[0]['title']}")

    except Exception as e:
        await update.message.reply_text(f"❌ **Error:** {str(e)}")
### PAUSE/RESUME COMMANDS ###
async def pause_song(update: Update, context: CallbackContext):
    await update.message.reply_text("⏸ **Playback Paused!**")

async def resume_song(update: Update, context: CallbackContext):
    await update.message.reply_text("▶️ **Playback Resumed!**")

### SKIP COMMAND ###
async def skip_song(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id in queue and len(queue[chat_id]) > 1:
        queue[chat_id].pop(0)
        next_song = queue[chat_id][0]
        await update.message.reply_text(f"⏭ **Skipped! Now Playing:** {next_song[1]}")
    else:
        await update.message.reply_text("⚠️ **No more songs in queue!**")

### QUEUE COMMAND ###
async def show_queue(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in queue or len(queue[chat_id]) == 0:
        await update.message.reply_text("⚠️ **The queue is empty!**")
        return

    msg = "🎵 **Current Queue:**\n"
    for i, song in enumerate(queue[chat_id]):
        msg += f"{i+1}. {song[1]}\n"

    await update.message.reply_text(msg)

### PLAYLIST COMMANDS ###
async def add_playlist(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ **Please provide a playlist name!**")
        return

    name = context.args[0]
    playlists[name] = []
    await update.message.reply_text(f"✅ **Playlist '{name}' created!**")

async def add_song_to_playlist(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ **Usage:** /addsong <playlist> <song>")
        return

    playlist = context.args[0]
    song = " ".join(context.args[1:])

    if playlist not in playlists:
        await update.message.reply_text(f"⚠️ **Playlist '{playlist}' does not exist!**")
        return

    playlists[playlist].append(song)
    await update.message.reply_text(f"🎵 **Added '{song}' to '{playlist}'!**")

async def remove_song_from_playlist(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ **Usage:** /removesong <playlist> <song>")
        return

    playlist = context.args[0]
    song = " ".join(context.args[1:])

    if playlist not in playlists or song not in playlists[playlist]:
        await update.message.reply_text(f"⚠️ **'{song}' is not in '{playlist}'!**")
        return

    playlists[playlist].remove(song)
    await update.message.reply_text(f"🗑 **Removed '{song}' from '{playlist}'!**")

async def delete_playlist(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ **Please provide a playlist name!**")
        return

    name = context.args[0]
    if name in playlists:
        del playlists[name]
        await update.message.reply_text(f"🗑 **Playlist '{name}' deleted!**")
    else:
        await update.message.reply_text(f"⚠️ **Playlist '{name}' does not exist!**")

### HELP COMMAND ###
async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "💖 **Nancy X Vibes - Command List** 💖\n\n"
        "🎶 **Music Commands** 🎶\n"
        "▶️ `/play <song>` - Play a song\n"
        "⏸ `/pause` - Pause the current song\n"
        "▶️ `/resume` - Resume playback\n"
        "⏭ `/skip` - Skip the current song\n"
        "📜 `/queue` - View the song queue\n\n"
        "⏳ `/playtime` - Check playtime of the current song\n\n"
        "📜 **Playlist Commands** 📜\n"
        "📜 `/viewplaylist <playlist>` - View playlist songs\n"
        "🎼 `/addplaylist <name>` - Create a playlist\n"
        "🎵 `/addsong <playlist> <song>` - Add a song\n"
        "❌ `/removesong <playlist> <song>` - Remove a song\n"
        "🗑 `/deleteplaylist <name>` - Delete a playlist\n\n"
        "✨ **Enjoy the vibes!** ✨"
    )
    await update.message.reply_text(help_text)

### VIEW PLAYLIST COMMAND ###
async def view_playlist(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ **Please provide a playlist name!**")
        return

    playlist = context.args[0]
    if playlist not in playlists or len(playlists[playlist]) == 0:
        await update.message.reply_text(f"⚠️ **Playlist '{playlist}' is empty or does not exist!**")
        return

    msg = f"📜 **Playlist: {playlist}**\n"
    for i, song in enumerate(playlists[playlist]):
        msg += f"{i+1}. {song}\n"

    await update.message.reply_text(msg)

### SONG PLAYTIME COMMAND ###
async def song_playtime(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in current_song:
        await update.message.reply_text("⚠️ **No song is currently playing!**")
        return

    title, duration = current_song[chat_id]
    await update.message.reply_text(f"🎵 **Currently Playing:** {title}\n⏳ **Duration:** {duration} seconds")

async def error_handler(update: Update, context: CallbackContext):
    print(f"❌ Error: {context.error}")  # Logs the error
    await update.message.reply_text("⚠️ An error occurred. Please try again.")

app.add_error_handler(error_handler)


### ENABLE/DISABLE FEATURES ###
async def enable_feature(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ **Please specify a feature to enable!**")
        return

    feature = context.args[0]
    await update.message.reply_text(f"✅ **Enabled '{feature}'!**")

async def disable_feature(update: Update, context: CallbackContext):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ **Please specify a feature to disable!**")
        return

    feature = context.args[0]
    await update.message.reply_text(f"🚫 **Disabled '{feature}'!**")
