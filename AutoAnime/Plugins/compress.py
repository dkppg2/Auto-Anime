import asyncio
import os
import time
import subprocess
import math
import logging
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from AutoAnime.FFMPEG.progress import *


async def en_co_de(dl, message):
  pron = dl.split("/")[-1]
  sox = pron.split(".")[-1]
  ul = pron.replace(f".{sox}", ".mkv")
  TF = time.time()
  progress = f"progress-{TF}.txt"
  # ffmpeg encoding code 
  cmd = f'''ffmpeg -hide_banner -loglevel quiet -progress """{progress}""" -i """{dl}""" -filter_complex "drawtext=fontfile=njnaruto(1).ttf:fontsize=30:fontcolor=white:bordercolor=black@0.50:x=10:y=10:box=1:boxcolor=black@0.5:boxborderw=6:text='Encoded By OngoingVoid':enable='between(t,0,15)':alpha='if(lt(t,14)\,1\,if(lt(t\,15)\,(1-(t-14))/1\,0))'" -metadata:s:a:0 title="OngoingVoid" -metadata:s:a:1 title="OngoingVoid" -metadata:s:s:0 title="OngoingVoid" -metadata:s:s:1 title="OngoingVoid" -metadata title="Uploaded By @OngoingVoid | Visit @AniVoid for completed animes." -map 0:v? -map 0:a? -map 0:s? -c:v libx265 -x265-params no-info=1 -crf 27.5 -s 1216x684 -b:v 420k -preset fast -threads 3 -pix_fmt yuv420p -tune animation -c:a libopus -profile:a aac_he -ac 2 -b:a 36k -c:s copy """{ul}""" -y'''
  await progress_shell(cmd, dl, progress, TF, message, "**ENCODING IN PROGRESS**")
 # logger.info("Started Encoding...")
  if os.path.lexists(ul):
    return ul
  else:
    return None
