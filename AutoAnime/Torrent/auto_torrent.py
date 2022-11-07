import asyncio
import logging
import anitopy
import glob
import os
import requests

from config import Config
from AutoAnime import TGBot
#from AutoAnime.FFMPEG.progress import *
#from AutoAnime.Torrent.encode_torrent import *
from AutoAnime.Plugins.rss import *
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from AutoAnime.Plugins.dictionary import Dict


async def auto_anime_dl(message):
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
  
  text = message.text
  if " " in text:
    link = text.split(" ", 1)[-1]
  elif message.reply_to_message:
    link = text
  else:
    return await message.reply_text("Send A Link To Get Processed", quote=True)
  if not os.path.isdir("downloads"):
    os.makedirs("downloads")
  m = await TGBot.send_message(chat_id=message.chat.id, text="Processing Your Link", reply_to_message_id=message.message_id)
  try:
    cmd = f'aria2c --dir="downloads" --seed-time=0 "{link}"'
    process = await asyncio.create_subprocess_shell(
      cmd,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE
    )
    stdout = await process.communicate()
    stderr = await process.communicate()
    logger.info(stdout)
    logger.info(stderr)
  except Exception as e:
    logger.info(e)
  dt_ = glob.glob("downloads/*")
  data = max(dt_, key=os.path.getctime)
  dat = data.replace("downloads/", '')
  old_name = anitopy.parse(dat)
  title_ = old_name["anime_title"]
  if "SubsPlease" in title_:
    title__ = title_.replace("SubsPlease", "")
    title_ = title__
  else:
    title_ = title_
  
  a = title_
  variables = {"search": a}
  
  json = (
   requests.post(url, json={"query": anime_query, "variables": variables}).json()["data"].get("Media", None)
  )
  eng_title = f"{json['title']['english']}"
  episode_ = old_name["episode_number"]
 # new_name = f"{episode_} - {eng_title} [720p] [Sub] @AniVoid.mkv"
 # os.rename(data, new_name)
  await m.edit_text("Successfully downloaded, now uploading At Specified Chat id...")
  await rss_app.send_document(chat_id=Config.CHAT_ID, document=data, caption=f"**{episode_} - {eng_title} [1080p] [Sub] @AniVoid**")
  await m.delete()
  #await TGBot.send_document(chat_id=Config.CHANNEL_ID, document=o)
  os.remove(data)
