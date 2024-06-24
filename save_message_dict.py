import json
import os
from datetime import datetime, timedelta
from aiogram.types import Message

MESSAGES_FILE = 'messages.json'
MAX_MESSAGE_AGE_DAYS = 14
tracked_reactions = ["👍", "👎", "❤", "🔥"]

if os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'r') as file:
        messages_data = json.load(file)
else:
    messages_data = {}


def save_message_data(msg: Message):
    messages_data[msg.message_id] = {
        'chat_id': msg.chat.id,
        'sender_id': msg.from_user.id,
        'date': msg.date.timestamp(), }
    with open(MESSAGES_FILE, 'w') as file:
        json.dump(messages_data, file)


def load_messages_data():
    global messages_data
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as file:
            messages_data = json.load(file)
    else:
        messages_data = {}


def cleanup_old_messages():
    global messages_data
    oldest_date = datetime.now() - timedelta(days=MAX_MESSAGE_AGE_DAYS)
    messages_data = {message_id: message for message_id, message in messages_data.items()
                     if datetime.fromtimestamp(message['date']) > oldest_date}
    with open(MESSAGES_FILE, 'w') as file:
        json.dump(messages_data, file)


def find_message_by_id(message_id):
    message = messages_data.get(message_id)
    if message:
        sender_id = message.get('sender_id')
        return message, sender_id
    return None, None
