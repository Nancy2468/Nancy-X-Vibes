from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

# Bot setup
bot = Client("NancyXBot")
call = PyTgCalls(bot)

# Database simulation (Replace with SQLite)
playlists = {}

# 🎵 Create a new playlist
@bot.on_message(filters.command(["ap", "addplaylist"]))
async def add_playlist(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: /ap <playlist_name>")
    
    name = args[1].strip()
    if name in playlists:
        return await message.reply("⚠ Playlist already exists!")
    
    playlists[name] = []
    await message.reply(f"✅ Playlist '{name}' created!")

# 🗑 Remove a playlist
@bot.on_message(filters.command(["rp", "removeplaylist"]))
async def remove_playlist(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: /rp <playlist_name>")
    
    name = args[1].strip()
    if name in playlists:
        del playlists[name]
        await message.reply(f"🗑 Playlist '{name}' removed!")
    else:
        await message.reply("⚠ Playlist not found!")

# 🎶 Add a song
@bot.on_message(filters.command(["as", "addsong"]))
async def add_song(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply("❌ Usage: /as <playlist> <song>")
    
    playlist, song = args[1], args[2]
    if playlist in playlists:
        playlists[playlist].append(song)
        await message.reply(f"🎶 Added to '{playlist}'!")
    else:
        await message.reply("⚠ Playlist not found!")

# ❌ Remove a song
@bot.on_message(filters.command(["rs", "removesong"]))
async def remove_song(client, message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply("❌ Usage: /rs <playlist> <song>")
    
    playlist, song = args[1], args[2]
    if playlist in playlists and song in playlists[playlist]:
        playlists[playlist].remove(song)
        await message.reply(f"🗑 Removed from '{playlist}'!")
    else:
        await message.reply("⚠ Song or playlist not found!")

# 📂 Show playlist (10 songs per page)
@bot.on_message(filters.command(["pl", "playlist"]))
async def show_playlist(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: /pl <playlist_name>")
    
    name = args[1].strip()
    if name not in playlists or not playlists[name]:
        return await message.reply("⚠ Playlist is empty or doesn't exist!")

    songs = playlists[name]
    text = f"🎵 **Playlist: {name}**\n\n" + "\n".join([f"🎶 {i+1}. {s}" for i, s in enumerate(songs[:10])])

    await message.reply(text)

# ▶ Play a song
@bot.on_message(filters.command("play"))
async def play_from_playlist(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply("❌ Usage: /play <playlist_name>")
    
    name = args[1].strip()
    if name not in playlists or not playlists[name]:
        return await message.reply("⚠ Playlist is empty or doesn't exist!")

    chat_id = message.chat.id
    song = playlists[name][0]  # Play first song

    await call.join_group_call(chat_id, AudioPiped(song))
    await message.reply(f"🎶 Playing {song} from '{name}'!")

# ⏸ Pause, Resume, Skip, Stop
@bot.on_message(filters.command("pause"))
async def pause_music(client, message):
    await call.pause_stream(message.chat.id)
    await message.reply("⏸ Music Paused!")

@bot.on_message(filters.command("resume"))
async def resume_music(client, message):
    await call.resume_stream(message.chat.id)
    await message.reply("▶ Resumed Music!")

@bot.on_message(filters.command("skip"))
async def skip_music(client, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏭ Skipped!")

@bot.on_message(filters.command("stop"))
async def stop_music(client, message):
    await call.leave_group_call(message.chat.id)
    await message.reply("🛑 Stopped Music!")

# 📥 Download MP3/MP4
@bot.on_message(filters.command("downloadmp3"))
async def download_mp3(client, message):
    await message.reply("🎵 Downloading MP3...")

@bot.on_message(filters.command("downloadmp4"))
async def download_mp4(client, message):
    await message.reply("📽 Downloading MP4...")

# 🆘 Help Command (Different for Users & Admins, Sent in DM)
@bot.on_message(filters.command("help"))
async def help_command(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Check if user is an admin
    admins = [admin.user.id for admin in await client.get_chat_members(chat_id, filter="administrators")]
    is_admin = user_id in admins

    if is_admin:
        help_text = (
            "**🔹 Admin Commands:**\n"
            "/play <playlist> - Play song\n"
            "/pause - Pause\n"
            "/resume - Resume\n"
            "/skip - Skip\n"
            "/stop - Stop music\n"
            "/queue - View queue\n\n"
            "/ap <name> - Add Playlist\n"
            "/rp <name> - Remove Playlist\n"
            "/as <playlist> <song> - Add Song\n"
            "/rs <playlist> <song> - Remove Song\n"
            "/pl <playlist> - Show Playlist\n\n"
            "/enable <feature> - Enable Feature\n"
            "/disable <feature> - Disable Feature\n"
        )
    else:
        help_text = (
            "**🔹 User Commands:**\n"
            "/play <playlist> - Play Song\n"
            "/pause - Pause\n"
            "/resume - Resume\n"
            "/skip - Skip\n"
            "/stop - Stop\n"
            "/queue - Show Queue\n\n"
            "/pl <playlist> - View Playlist\n"
            "/downloadmp3 <url> - Download MP3\n"
            "/downloadmp4 <url> - Download MP4\n"
        )

    # Send help in private DM
    try:
        await client.send_message(user_id, help_text)
        await message.reply("📩 **Check your DM for help!**")
    except:
        await message.reply("❌ **Unable to send DM. Please enable private messages!**")

# Start Bot
bot.run()
