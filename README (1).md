# Telegram Music Bot

A comprehensive Telegram bot that can play songs on video chats, voice chats, group chats, and live streams. It also sends good morning and good night wishes, handles song requests, welcomes new members, informs about members leaving, and more.

## Features
- Play music in video chats, voice chats, group chats, and live streams.
- Send good morning and good night wishes at specific times.
- Respond to greetings (e.g., "good morning", "good night", etc.) from admins and owners.
- Prompt the last song requester to play more songs if the queue is empty.
- Welcome new members and inform about members who leave the group.
- Send emojis and stickers after every song request.
- Admin functionalities to manage a permanent playlist.
- Admin functionalities to manage the song queue (change song position, remove songs).
- Download songs from YouTube in MP3 or MP4 format.
- Store and manage playlists using SQLite.
- Store and retrieve additional user information (e.g., Date of Birth).
- Play, pause, resume, stop, seek, and set volume for songs.
- Auto stop songs if inactive for 6 minutes and resume or restart on new song requests.
- Multi-group support with individual settings.
- Attractive start message with animation.

## Setup and Installation

1. **Create a Telegram Bot:**
   - Open Telegram and search for `BotFather`.
   - Create a new bot and get the bot token.

2. **Set Up Project Environment:**
   - Install Python 3.7+
   - Install necessary libraries:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configuration:**
   - Create a `config.py` file and add your bot token and other configurations.

4. **Run the Bot:**
   - Execute the main bot script:
     ```bash
     python bot.py
     ```

## Files

- `bot.py`: Main bot script.
- `config.py`: Configuration file with bot token and other settings.
- `database.py`: SQLite database management.
- `handlers.py`: Handlers for various bot commands and events.
- `scheduler.py`: Scheduling messages.
- `queue.py`: Queue management for song requests.
- `members.py`: Member management functionalities.

## Usage

- Start the bot with `/start`.
- Admins can manage the permanent playlist using `/addsong <song>`, `/removesong <song_id>`, and `/showplaylist`.
- Admins can manage the queue using `/managequeue change <old_index> <new_index>` or `/managequeue remove <index>`.
- Download songs from YouTube using `/download <URL> <mp3|mp4>`.
- When a member joins or leaves, the bot sends a message with the user's name, ID, and date of birth (if available).
- Control song playback with `/play`, `/pause`, `/resume`, `/stop`, `/seek <seconds>`, and `/setvolume <level>`.
- Skip the current song with `/skip`.
- The bot will automatically stop songs if there is no activity in video chat, voice chat, group chat, or live stream for 6 minutes.