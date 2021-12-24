from bot import Bot
from constants import BTN_COURSES, MESSAGES
from config import INVITE_LINK
from helper_functions import subscribed, can_user_get_lessons
from pyrogram import filters
import time
from dbase import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Bot.on_message(filters.private & subscribed & can_user_get_lessons)
async def send_lessons(client, message):
	category_id = 0
	for i in db.CATEGORY:
		if message.text == i.name:
			category_id = i.id
			break

	if category_id == 0:
		return
	for i in db.get_lessons(category_id):
		await client.copy_message(message.chat.id,
			from_chat_id=i[2], message_id=i[3])
		time.sleep(0.037)

@Bot.on_message(filters.private & ~subscribed & filters.text & ~filters.command("start"))
async def go_and_subscribe_(client, message):
	await message.reply(text=MESSAGES["not_subscribed"],
		reply_markup=InlineKeyboardMarkup([
				[
					InlineKeyboardButton(text="Kanalga qo'shilish", url=INVITE_LINK)
				],
				[
					InlineKeyboardButton(text="Tekshirish", callback_data="check_subscription")
				]
			]))
