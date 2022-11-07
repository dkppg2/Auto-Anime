from AutoAnime import TGBot
import logging
import asyncio 
import time
import pickle # to dumps/loads 
import codecs # to encode/decode basically
#import requests
from AutoAnime.DB.redis import myDB

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from AutoAnime.Plugins.dictionary import Dict
from AutoAnime.Torrent.auto_torrent import auto_anime_dl
from AutoAnime.Plugins.bash import *
from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.handlers import MessageHandler, CallbackQueryHandler

from pyrogram.errors import FloodWait
from datetime import datetime as dt

from config import Config
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from AutoAnime.Plugins.ls import l_s
from AutoAnime.Plugins.queue import *
from AutoAnime.Plugins.eval import *
@TGBot.on_message(filters.command("start", prefixes=["/", "."]))
async def start_cmd_handler(bot, message):
  if message.from_user.id not in Config.AUTH_USERS:
    return
  await message.reply_text(
    text=Dict.START,
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton("📕Channel", url="https://t.me/AniVoid")
        ],
      ],
    ),
    parse_mode="md"
  )
@TGBot.on_message(filters.command("encode", prefixes=["/", "."]))
async def work_auto_shit(bot, message):
  if message.from_user.id not in Config.AUTH_USERS:
    return
  await auto_anime_dl(message)



@TGBot.on_message(filters.incoming & filters.command("ls", prefixes=["/", "."]))
async def lost_files(bot, message):
  if message.from_user.id not in Config.AUTH_USERS:
    return
  await l_s(bot, message)


@TGBot.on_message(filters.incoming & filters.command("eval", prefixes=["/", "."]))
async def l_ost_files(bot, message):
  await eval_handler(bot, message)

@TGBot.on_message(filters.incoming & (filters.video | filters.document))
async def wah_1_man(bot, message: Message):
  if message.from_user.id not in Config.AUTH_USERS:
    return
  query = await message.reply_text("Aᴅᴅᴇᴅ ᴛʜɪs ғɪʟᴇ ɪɴ ǫᴜᴇᴜᴇ.\nCᴏᴍᴘʀᴇss ᴡɪʟʟ sᴛᴀʀᴛ sᴏᴏɴ.", quote=True)
  a = message # using a as message is easy
  pickled = codecs.encode(pickle.dumps(a), "base64").decode()
  myDB.rpush("DBQueue", pickled)
  if myDB.llen("DBQueue") == 1:
    await query.delete()
    await add_task(bot, message)

@TGBot.on_message(filters.incoming & filters.command("bash", prefixes=["/", "."]))
async def _l_ost_files(bot, message):
  if message.from_user.id not in Config.AUTH_USERS:
    return
  await bash_exec(bot, message)
