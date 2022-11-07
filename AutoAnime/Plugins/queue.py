import os
import logging
import pickle
import codecs
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from pyrogram.types import Message
from AutoAnime.DB.redis import myDB
from AutoAnime.Plugins.labour import *
async def on_task_complete(bot, message: Message):
  #del queue.data[0]
  myDB.lpop("DBQueue")
  queue_ = myDB.lindex("DBQueue", 0)
  if queue_ is None:
    return
  _queue = pickle.loads(codecs.decode(queue_.encode(), "base64"))
  value_ = myDB.llen("DBQueue")
  if value_ is None:
    return
  elif value_ > 0:
    await add_task(bot, _queue)

async def add_task(bot, message: Message):
  try:
    os.system('rm -rf /app/downloads/*')
    await labour_encode(bot, message)
  except Exception as e:
    logger.info(e)
  value_ = myDB.llen("DBQueue")
  if value_ is None:
    return
  await on_task_complete(bot, message)
  
