from . import TGBot
import logging
import asyncio
import codecs 
import pickle 
import time
from pyrogram import Client, filters, idle
from AutoAnime.Plugins.rss import rss_app
from AutoAnime.DB.redis import *
from AutoAnime.Plugins.queue import *


logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def resume_task():
  if myDB.llen("DBQueue") > 0:
    queue_ = myDB.lindex("DBQueue", 0)
    _queue = pickle.loads(codecs.decode(queue_.encode(), "base64"))
    await add_task(TGBot, _queue)

async def start_bot():
  await rss_app.start()
  await TGBot.start()
  await resume_task()
  await idle()
  await rss_app.start()
  await TGBot.stop()
  
if __name__ == "__main__":
  print("Starting up...")
  asyncio.get_event_loop().run_until_complete(start_bot())
