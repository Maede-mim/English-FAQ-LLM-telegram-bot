import telebot
from dotenv import load_dotenv
import os
from src.constants import WELCOME_MESSAGE , WAITING_MESSAGE
from src.db import DBHandler
from src.llm import call_llm
from loguru import logger

load_dotenv()

ADMIN_USERNAME = [
    username.strip().lower()
    for username in os.getenv("ADMIN_USERNAME", "").split(",")
]

VALID_CHATS = [
    chat.strip().lower()
    for chat in os.getenv("VALID_CHATS", "").split(",")
]
  
logger.info(f"ADMIN_USERNAME:{ADMIN_USERNAME}")
logger.info(f"VALID_CHATS:{VALID_CHATS}")
# Initialize bot with HTML parsing
bot = telebot.TeleBot(token=os.getenv("BOT_TOKEN"), parse_mode="markdown")
db_handler = DBHandler()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Sends a welcome message when user sends /start or /help.~
    """
    bot.reply_to(message, WELCOME_MESSAGE)

def is_valid_admin_reply(message):
    """
    Responds only to admin replies, showing the original message content.
    Safely handles missing user/chat data.
    """
    username = message.user.username.lower()
    chat_username = message.chat.username.lower()
    is_admin = username in ADMIN_USERNAME
    is_valid_chat =chat_username in VALID_CHATS
    logger.info(f"ADMIN_USERNAME:{ADMIN_USERNAME}")
    logger.info(f"VALID_CHATS:{VALID_CHATS}")

    return is_admin, is_valid_chat

@bot.message_handler(func=lambda  messege:True)
def store_message(message):
    json_data = message.json
    db_handler.store_message(json_data)
    print(f"store message by ID:{json_data.get('message_id')}")



@bot.message_reaction_handler(
        func= lambda message:message.new_reaction and is_valid_admin_reply(message))
def handle_reaction(message: telebot.types.Message):
    reaction = None
    if getattr(message, 'new_reaction', None):
        reaction = message.new_reaction[-1].emoji
    if reaction not in ['👍']:
        return

    # Safely fetch the original text
    original = db_handler.get_message(message.message_id)
    message_text = original.get("text") if original else None
    if not message_text:
        return

    reply_msg = bot.reply_to(message , WAITING_MESSAGE)
    response = call_llm(message_text)
    bot.edit_message_text(chat_id=reply_msg.chat.id, message_id=reply_msg.id, text=response)


def main():
    """
    Starts the bot polling loop.
    """
    print("BOT_RUNNING...")
    bot.infinity_polling(
        allowed_updates=['message','message_reaction'],
                         restart_on_change=True)

if __name__ == "__main__":
    main()

