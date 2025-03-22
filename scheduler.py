import schedule
import time
from datetime import datetime
from telegram import Bot
from config import GOOD_MORNING_TIME, GOOD_NIGHT_TIME

GOOD_MORNING_MESSAGES = [
    """🌸 **Good Morning, Beautiful Soul!** 🌸\n\n💖 May your day be filled with **smiles, love, and happiness**. ☀️✨\n🌿 Let the sunshine warm your heart, and may **positivity** follow you everywhere! 🌞🌼\n\n☕ **Here’s a cup of joy, just for you!** ☕💛\n🎶 *Have a peaceful and melodious day!* 🎶""",
    """🌞 **Rise and Shine!** 🌞\n\n💖 A brand-new day is waiting for you! 🌈✨\n🌿 Embrace the morning with a **smile, hope, and love**. May today bring you **happiness and success**! 🌼💫\n\n☕ **Take a sip of happiness and enjoy your day!** ☕💛"""
                     ]
Good_Night_Message = [
    """🌙 **Good Night, Sweet Soul!** 🌙\n\n✨ The stars are whispering **beautiful dreams** just for you. 🌟💖\n💤 May your heart be light, your worries fade, and your sleep be **peaceful like a lullaby**. 🎶💫\n\n🌷 **Close your eyes and wake up refreshed to a new day!** 🌌💖""",
    """💫 **Sweet Dreams, [User's Name]!** 💫\n\n🌙 Let go of worries, relax your mind, and drift into a **world of dreams and peace**. 🌿💖\n✨ May your night be filled with **comfort and love**. 😴💫\n\n🌟 **Sleep tight! Tomorrow is a new blessing!** 💖"""
]
    
     
chat_id = '7598019677'  # Replace with your chat ID

async def send_good_morning(bot, chat_id: int):
    message = random.choice(GOOD_MORNING_MESSAGES)
    await bot.send_message(chat_id=chat_id, text=message)

async def send_good_night(bot, chat_id: int):
    message = random.choice(GOOD_NIGHT_MESSAGES)
    await bot.send_message(chat_id=chat_id, text=message)
