import telebot
from config import BOT_TOKEN
from User_action import UserActions

user_actions = UserActions()
bot = telebot.TeleBot(BOT_TOKEN)

