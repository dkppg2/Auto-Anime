import os
import dotenv

dotenv.load_dotenv()

class Config(object):
  API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
      BOT_TOKEN = os.environ.get("BOT_TOKEN")
        AUTH_USERS = os.environ.get("AUTH_USERS")
          STRING_SESSION = os.environ.get("STRING_SESSION")
            CHANNEL_ID = os.environ.get("CHANNEL_ID")
              RSS_URL = os.environ.get("RSS_URL")
                CHAT_ID = os.environ.get("CHAT_ID")
                  REDIS_HOST = os.environ.get("REDIS_HOST")
                    REDIS_PASS = os.environ.get("REDIS_PASS")

Config.AUTH_USERS = [2067727305]
Config.API_ID = 14604313
Config.API_HASH = "a8ee65e5057b3f05cf9f28b71667203a"
Config.BOT_TOKEN = "5433519682:AAGalXAhE4h2FuVBTnJTsyIOPo6xYgH1UwY"
Config.STRING_SESSION = "BQAB0CBnIg2uVnxLqsV1sRAkg8HPTymRpDzZ1D87BWOiRp7lrkon40NiRVqcnE2EjGSTMI5GUBg2IwF4ait2_jDLtLqpWJrPMPEJzWNiHZKS4_CTpwwl6YZ1_fOKhJfFGETxzIB2OaukcSNsf9LOlXNJEKfKyq10xzsP7ztJwq-qZHe-LRguFjlMk6X8gTX2ge8TLQVr4Qq0aJ-62eaDQ1CvtxNiqqUUjjRcTIVNjBj6cs_BLh5YaGcyIQ2hWWFJHAzpXoHkqe9_H-M2_yzpnHowtskm1HJzLTWc1ZNccWmhcsQIuQeirWldOW8quUpzs4dgFjumomQRNlOLce_NnG_iez8DyQA"
Config.CHANNEL_ID = -1001537403612
Config.RSS_URL = "Subsplease"
Config.CHAT_ID = -1005433519682
Config.REDIS_HOST = "redis-19612.c8.us-east-1-3.ec2.cloud.redislabs.com"
Config.REDIS_PASS = "LD8PjDdA6zqijQoazGod4u6FXdavTrtj"
REDIS_PORT = "19612"
