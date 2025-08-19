import os
import sys
import random
import logging
import re
from collections import defaultdict
from threading import Thread
import telebot
import instaloader
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app to keep the bot alive
app = Flask(__name__)

@app.route('/')
def home():
    return "I'm alive"

def run_flask_app():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask_app)
    t.start()

# Start the Flask app in a thread 
keep_alive()

# Initialize the Telegram bot
API_TOKEN = os.getenv("API_TOKEN")
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(API_TOKEN)

# In-memory list to store user IDs
user_ids = set()

def add_user(user_id):
    user_ids.add(user_id)

def remove_user(user_id):
    user_ids.discard(user_id)

def get_all_users():
    return list(user_ids)

# List of keywords for different report categories
report_keywords = {
    "HATE": ["devil", "666", "savage", "love", "hate", "followers", "selling", "sold", "seller", "dick", "ban", "banned", "free", "method", "paid"],
    "SELF": ["suicide", "blood", "death", "dead", "kill myself"],
    "BULLY": ["@"],
    "VIOLENT": ["hitler", "osama bin laden", "guns", "soldiers", "masks", "flags"],
    "ILLEGAL": ["drugs", "cocaine", "plants", "trees", "medicines"],
    "PRETENDING": ["verified", "tick"],
    "NUDITY": ["nude", "sex", "send nudes"],
    "SPAM": ["phone number", "email", "contact"]
}

def check_keywords(text, keywords):
    return any(keyword in text.lower() for keyword in keywords)

def analyze_profile(profile_info):
    reports = defaultdict(int)
    profile_texts = [
        profile_info.get("username", ""),
        profile_info.get("biography", ""),
    ]

    for text in profile_texts:
        for category, keywords in report_keywords.items():
            if check_keywords(text, keywords):
                reports[category] += 1

    if reports:
        unique_counts = random.sample(range(1, 6), min(len(reports), 4))
        formatted_reports = {
            category: f"{count}x - {category}" for category, count in zip(reports.keys(), unique_counts)
        }
    else:
        all_categories = list(report_keywords.keys())
        num_categories = random.randint(2, 5)
        selected_categories = random.sample(all_categories, num_categories)
        unique_counts = random.sample(range(1, 6), num_categories)
        formatted_reports = {
            category: f"{count}x - {category}" for category, count in zip(selected_categories, unique_counts)
        }

    return formatted_reports

def get_public_instagram_info(username):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        info = {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "follower_count": profile.followers,
            "following_count": profile.followees,
            "is_private": profile.is_private,
            "post_count": profile.mediacount,
            "external_url": profile.external_url,
        }
        return info
    except instaloader.exceptions.ProfileNotExistsException:
        return None
    except instaloader.exceptions.InstaloaderException as e:
        logging.error(f"An error occurred: {e}")
        return None

def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(f"@{FORCE_JOIN_CHANNEL}", user_id)
        return member.status in ['member', 'administrator', 'creator']
    except telebot.apihelper.ApiTelegramException:
        return False

def escape_markdown_v2(text):
    # Escape special MarkdownV2 characters
    replacements = {
        '_': r'\_', '*': r'\*', '[': r'\[', ']': r'\]',
        '(': r'\(', ')': r'\)', '~': r'\~', '`': r'\`',
        '>': r'\>', '#': r'\#', '+': r'\+', '-': r'\-',
        '=': r'\=', '|': r'\|', '{': r'\{', '}': r'\}',
        '.': r'\.', '!': r'\!'
    }
    pattern = re.compile('|'.join(re.escape(key) for key in replacements.keys()))
    return pattern.sub(lambda x: replacements[x.group(0)], text)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not is_user_in_channel(user_id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_JOIN_CHANNEL}"))
        markup.add(telebot.types.InlineKeyboardButton("Joined", callback_data='reload'))
        bot.reply_to(message, f"Please join @{FORCE_JOIN_CHANNEL} to use this bot.", reply_markup=markup)
        return

    add_user(user_id)  # Add user to the list
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Help", callback_data='help'))
    markup.add(telebot.types.InlineKeyboardButton("Update Channel", url='t.me/PythonBotz'))
    bot.reply_to(message, "Welcome! Use /getmeth <username> to analyze an Instagram profile.\n\n 100% working Too in $30 message @SugerBaddie !!", reply_markup=markup)

@bot.message_handler(commands=['getmeth'])
def analyze(message):
    user_id = message.chat.id
    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"Please join @{FORCE_JOIN_CHANNEL} to use this bot.")
        return

    username = message.text.split()[1:]  # Get username from command
    if not username:
        bot.reply_to(message, "😾 Worong method Please send like this /getmeth Username without @ & < >  Send your Target username.")
        return

    username = ' '.join(username)
    bot.reply_to(message, f"🔍 Scanning Your Target Profile: {username}. Please wait...")

    profile_info = get_public_instagram_info(username)
    if profile_info:
        reports_to_file = analyze_profile(profile_info)
        result_text = f"**Public Information for {username}:**\n"
        result_text += f"Username: {profile_info.get('username', 'N/A')}\n"
        result_text += f"Full Name: {profile_info.get('full_name', 'N/A')}\n"
        result_text += f"Biography: {profile_info.get('biography', 'N/A')}\n"
        result_text += f"Followers: {profile_info.get('follower_count', 'N/A')}\n"
        result_text += f"Following: {profile_info.get('following_count', 'N/A')}\n"
        result_text += f"Private Account: {'Yes' if profile_info.get('is_private') else 'No'}\n"
        result_text += f"Posts: {profile_info.get('post_count', 'N/A')}\n"
        result_text += f"External URL: {profile_info.get('external_url', 'N/A')}\n\n"
        result_text += "Suggested Reports for Your Target:\n"
        for report in reports_to_file.values():
            result_text += f"• {report}\n"
        result_text += "\n*Note: This method is based on available data and may not be fully accurate.*\n\n for supporting my devloper please donate some Money @SendPayments"

        # Escape special characters for MarkdownV2
        result_text = escape_markdown_v2(result_text)

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Visit Target Profile", url=f"https://instagram.com/{profile_info['username']}"))
        markup.add(telebot.types.InlineKeyboardButton("Developer", url='t.me/SugerBaddie'))

        bot.send_message(message.chat.id, result_text, reply_markup=markup, parse_mode='MarkdownV2')
    else:
        bot.reply_to(message, f"❌ Profile {username} not found or an error occurred.")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    broadcast_message = message.text[len("/broadcast "):].strip()
    if not broadcast_message:
        bot.reply_to(message, "Please provide a message to broadcast.")
        return

    users = get_all_users()
    for user in users:
        try:
            bot.send_message(user, broadcast_message)
        except Exception as e:
            logging.error(f"Failed to send message to {user}: {e}")

@bot.message_handler(commands=['users'])
def list_users(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    users = get_all_users()
    if users:
        user_list = "\n".join([f"User ID: {user_id}" for user_id in users])
        bot.reply_to(message, f"List of Users:\n{user_list}")
    else:
        bot.reply_to(message, "No users found.")

@bot.message_handler(commands=['remove_user'])
def remove_user_command(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    user_id = message.text.split()[1:]  # Get user ID from command
    if not user_id:
        bot.reply_to(message, "Please provide a user ID.")
        return

    user_id = int(user_id[0])
    remove_user(user_id)
    bot.reply_to(message, f"User ID {user_id} has been removed.")

@bot.message_handler(commands=['restart'])
def restart_bot(message):
    if str(message.chat.id) != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    bot.reply_to(message, "Bot is restarting...")
    logging.info("Bot is restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.callback_query_handler(func=lambda call: call.data == 'reload')
def reload_callback(call):
    user_id = call.from_user.id
    if is_user_in_channel(user_id):
        bot.answer_callback_query(call.id, text="You are now authorized to use the bot!")
        bot.send_message(user_id, "You are now authorized to use the bot. Use /getmeth <username> to analyze an Instagram profile.")
    else:
        bot.answer_callback_query(call.id, text="You are not a member of the channel yet. Please join the channel first.")

@bot.callback_query_handler(func=lambda call: call.data == 'help')
def help_callback(call):
    help_text = "Here's how you can use this bot:\n\n"
    help_text += "/getmeth <username> - Analyze an Instagram profile.\n"
    help_text += "Make sure you are a member of the channel to use this bot."
    
    # Escape special characters for MarkdownV2
    help_text = escape_markdown_v2(help_text)

    bot.answer_callback_query(call.id, text=escape_markdown_v2(help_text))
    bot.send_message(call.from_user.id, help_text, parse_mode='MarkdownV2')

if __name__ == "__main__":
    print("Starting the bot...")
    logging.info("Bot started.")
    
    # Start the bot polling in a separate thread
    t = Thread(target=bot.polling)
    t.start()


