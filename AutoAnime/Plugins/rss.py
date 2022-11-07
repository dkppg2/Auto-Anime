import os
import logging
import sys
import feedparser
from AutoAnime.DB.redis import myDB
from time import sleep, time
from datetime import datetime as dt
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
from time import sleep

#blocking running apscheduler thing
logging.getLogger('apscheduler').setLevel(logging.CRITICAL + 10)


feed_urls = f"https://nyaa.si/?page=rss&u={Config.RSS_URL}"



plugins = dict(root="AutoAnime/Plugins")
rss_app = Client(
  session_name=Config.STRING_SESSION,
  api_id=Config.API_ID,
  plugins=plugins,
  api_hash=Config.API_HASH
  #session_string=Config.STRING_SESSION
)

#pop = []
def send_msg(msg):
  print("Source was released on Subsplease.org, fetching links....")
  try:
    rss_app.send_message(chat_id=Config.CHAT_ID, text=f"/encode {msg}")
    myDB.rpush("RSS_DB", msg)
  except FloodWait as e:
    print(f"FloodWait: {e.x} Seconds")
    sleep(e.x)
  except Exception as e:
    print(e)
    

def main_working():
  data = myDB.lrange("RSS_DB", 0, -1)
  FEED = feedparser.parse("https://subsplease.org/rss/?t&r=1080")
  if len(FEED.entries) == 0:
    return
  entry = FEED.entries[0]
  
  if entry.link in data:
    return
  elif "[Batch]" in entry.title:
      return
  else:
    send_msg(entry.link)
    print("I have done my job - sending torrent link.")

scheduler = BackgroundScheduler()

#scheduler.add_job(main_working, "interval", seconds=30, max_instances=30)
scheduler.add_job(main_working, trigger="interval", seconds=180)
scheduler.start()
