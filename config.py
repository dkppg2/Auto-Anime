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
  

Config.AUTH_USERS = [5126929234, 1930343434]
Config.API_ID = 3281305
Config.API_HASH = "a9e62ec83fe3c22379e3e19195c8b3f6"
Config.BOT_TOKEN = "5471694952:AAEWi7UhF_neZRC4SJVPhGREJgikrB0MCP0"
Config.STRING_SESSION = "AQCwR63zSaQD1xOPDCfGRUJxpYUMwmZyGj7Fd9OvUFJR4twLFamCJ7FVyiETBglKFKXHmI73Y7Yhdu2XO5Um957rgIXB1M0Y9wZLL7L7c5V9bME08fhNVXOQYTBxkbxgWjVez4NKzNxt-Zm6Udrl6G9bMpfxyWUV_kQ8gC8c_z2C-tZwrzK292g5mpR8RE7lHpkkH6iOXsZY_Zpr6iTkIfDWE06ZCC3gumTPJ8pMYdAtSxLzq3frT3eMyx-nVT7NLZSCmUfHYTM5CfWyDZB3-BA90evyMUIefgso6DN7A1snXWX6va0qrdywZ2-KVE9_3ezitwv5X5vZHLsXSkjwBxVbAAAAATGWu1IA"
Config.CHANNEL_ID = -1001315246742
Config.RSS_URL = "Subsplease"
Config.CHAT_ID = -1001541090367
Config.REDIS_HOST = "redis-19612.c8.us-east-1-3.ec2.cloud.redislabs.com"
Config.REDIS_PASS = "LD8PjDdA6zqijQoazGod4u6FXdavTrtj"
REDIS_PORT = "19612"
