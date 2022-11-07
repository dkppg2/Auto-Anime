import os
from AutoAnime import TGBot
import string
import time
import asyncio 
from config import Config
import anitopy
import requests
#from SmartEncoder.__main__ import *

from AutoAnime.Plugins.compress import en_co_de
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from AutoAnime.FFMPEG.dl_progress import *
#from SmartEncoder.Plugins.list import *

import requests

url = "https://graphql.anilist.co"
anime_query = """
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
"""

async def send_info(image, caption, title, ani_id):
  cap = caption.replace("ep_tit", title)
  link = f"https://anilist.co/anime/{ani_id}"
  await TGBot.send_photo(
    chat_id=Config.CHANNEL_ID,
    photo=image,
    caption=cap,
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton("📚 Synopsis", url=link)
        ],
      ],
    ),
    parse_mode="md"
  )

async def labour_encode(bot, update):
  download_location = "downloads" + "/"
  sent_message = await bot.send_message(
    text="**DOWNLOADING**",
    chat_id=update.chat.id,
    reply_to_message_id=update.message_id
  )
  c_time = time.time()
  f_n = await bot.download_media(
    message=update,
    #myDB.lindex("DBQueue", 0),
    #file_name=download_location,
    progress=progress_for_pyrogram,
    progress_args=(
      bot,
      "**DOWNLOADING**",
      sent_message,
      c_time
    )
  )
  logger.info(f_n)
  await asyncio.sleep(1)
  if f_n is not None:
    await sent_message.edit_text("**TRYING TO ENCODE**")
  # if not .mkv or.mp4 or .webm
  if f_n.rsplit(".", 1)[-1].lower() not in ["mkv", "mp4", "webm", "avi"]:
    return await sent_message.edit_text("This format isnt allowed , please send only either **MKV** or **MP4** files.")
  # if in .mkv or .mp4 
  if "`" in f_n:
    _f_n = f_n.replace("`", "'")
    os.rename(f_n, _f_n)
  elif '"' in f_n:
    _f_n = f_n.replace("`", "'")
    os.rename(f_n, _f_n)
  else:
    _f_n = f_n
  o = await en_co_de(
    _f_n,
    sent_message
  )
  logger.info(o)
  # upload event 
  if o is None:
    await sent_message.edit_text("Either the current ffmpeg code didnt work on the file as it gave error or its an internal issue.\nContact the [dev](https://t.me/Bro_isDarkal)",
    disable_web_page_preview=True)
    os.remove(_f_n)
    return
  if o is not None:
    await sent_message.edit_text("UPLOADING")
    upload = await bot.send_document(
      chat_id=update.chat.id,
      document=o,
      force_document=True,
      #caption="©️ @Animes_Encoded",
      reply_to_message_id=update.message_id,
      progress=progress_for_pyrogram,
      progress_args=(bot, "UPLOADING", sent_message, c_time)
    )
    old_name = anitopy.parse(o)
    title_ = old_name["anime_title"]
    episode_ = old_name["episode_number"]
    new_name = f"{episode_} - {title_} [720p] [Sub] @OngoingVoid.mkv"
    os.rename(o, new_name)
    if "SubsPlease" in title_:
      t = title_.replace("SubsPlease", "")
    else:
      t = title_
      
    try:
      s_e = old_name["anime_season"]
      tope = f"{t} S{s_e}"
    except KeyError as error:
      tope = f"{t}"
    variables = {"search": tope}
    json = (
      requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
    )
    id_ = json["id"]
    pic_url = f"https://img.anili.st/media/{id_}"
    gen = json["genres"]
    msg = "Genres : "
    for x in gen:
      msg += f"{x}, "
    m_ = msg.rsplit(',', 1)[0]
    try:
      variables = {"search": tope}
      json = (
        requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
      )
      s = old_name["anime_season"]
      idd = json["id"]
      text = f"**📌 [```{idd}```] ep_tit S{s} - {episode_} was released\n━━━━━━━━━━━━━━\n➜ 🎵 Audio : Japanese\n➜ 📂 Quality : 720p\n➜ 🎭 {m_}\n━━━━━━━━━━━━━━**"
    except KeyError as error:
      variables = {"search": tope}
      json = (
        requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
      )
      ohm = json["id"]
      text = f"**📌 [```{ohm}```] ep_tit - {episode_} was released\n━━━━━━━━━━━━━━\n➜ 🎵 Audio : Japanese\n➜ 📂 Quality : 720p\n➜ 🎭 {m_}\n━━━━━━━━━━━━━━**"
      
    if "SubsPlease" in title_:
      try:
        title__ = title_.replace("SubsPlease", "")
        season = old_name["anime_season"]
        a = title__
        variables = {"search": a}
        json = (
          requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
        )
        eng_title = f"{json['title']['english']}"
        if eng_title == "None":
          eng_title = title__
        sax = string.capwords(eng_title)
        _name = f"{episode_} - {sax} S{season} [720p] [Sub] @OngoingVoid.mkv"
        os.rename(new_name, _name)
        #await bot.send_message(chat_id=Config.CHANNEL_ID, text=f"<b>• Anime - {eng_title}\n• Season - {season}\n• Episode - {episode_}\n• Quality - 720p</b>", parse_mode="html")
        await send_info(pic_url, text, sax, json["id"])
        await bot.send_document(chat_id=Config.CHANNEL_ID, document=_name)
        os.remove(_name)
      except KeyError as error:
        title__ = title_.replace("SubsPlease", "")
        a = title__
        variables = {"search": a}
        json = (
          requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
        )
        eng_title = f"{json['title']['english']}"
        if eng_title == "None":
          eng_title = title__
        sax = string.capwords(eng_title)
        #season = old_name["anime_season"]
        _name = f"{episode_} - {sax} [720p] [Sub] @OngoingVoid.mkv"
        os.rename(new_name, _name)
        #await bot.send_message(chat_id=Config.CHANNEL_ID, text=f"<b>• Anime - {eng_title}\n• Episode - {episode_}\n• Quality - 720p</b>", parse_mode="html")
        await send_info(pic_url, text, sax, json["id"])
        await bot.send_document(chat_id=Config.CHANNEL_ID, document=_name)
    else:
      try:
        season = old_name["anime_season"]
        a = title_
        variables = {"search": a}
        json = (
          requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
        )
        eng_title = f"{json['title']['english']}"
        if eng_title == "None":
          eng_title = title_
        if title_ == "Overlord IV":
          sax = eng_title
        else:
          sax = string.capwords(eng_title)
        _name = f"{episode_} - {sax} S{season} [720p] [Sub] @OngoingVoid.mkv"
        os.rename(new_name, _name)
        #await bot.send_message(chat_id=Config.CHANNEL_ID, text=f"<b>• Anime - {eng_title}\n• Season - {season}\n• Episode - {episode_}\n• Quality - 720p</b>", parse_mode="html")
        await send_info(pic_url, text, sax, json["id"])
        await bot.send_document(chat_id=Config.CHANNEL_ID, document=_name)
        os.remove(_name)
      except KeyError as error:
        a = title_
        variables = {"search": a}
        json = (
          requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
        )
        eng_title = f"{json['title']['english']}"
        if eng_title == "None":
          eng_title = title_
        if title_ == "Overlord IV":
          sax = eng_title
        else:
          sax = string.capwords(eng_title)
        _name = f"{episode_} - {sax} [720p] [Sub] @OngoingVoid.mkv"
        #await bot.send_message(chat_id=Config.CHANNEL_ID, text=f"<b>• Anime - {eng_title}\n• Episode - {episode_}\n• Quality - 720p</b>", parse_mode="html")
        await send_info(pic_url, text, sax, json["id"])
        os.rename(new_name, _name)
        await bot.send_document(chat_id=Config.CHANNEL_ID, document=_name)
        os.remove(_name)
    # remove uploaded file as it will free space
    await bot.send_sticker(chat_id=Config.CHANNEL_ID, sticker="CAACAgEAAxkBAAI0aWKx36P2GY9Fq6xvN0SBU1V2xZYIAAKXAgACJ_hhR9HcWzoditT7HgQ")
    #os.remove(o)
    os.remove(_f_n)
    # in order to make bot organised 
    await sent_message.delete()
