from bot import Bot
from constants import BACK, UserStatus, MESSAGES,\
	ADMIN_MENU, USER_MENU, BTN_COURSES, BTN_ABOUT, BTN_STATISTIC
from pyrogram import filters
from config import ADMINS
from dbase import db
from helper_functions import is_admin_free, is_user_free,\
	subscribed
from pyrogram.types import ReplyKeyboardMarkup

#foydalanuvchi va admin uchun umumiy menyular
#Ortga
@Bot.on_message(filters.private & filters.regex(BACK))
async def back_to_main(client, message):
	if message.chat.id in ADMINS:
		db.update_admin(message.chat.id, status=UserStatus.FREE)
		await client.send_message(message.chat.id, MESSAGES["main_menu"],
			reply_markup=ADMIN_MENU)
	else:
		db.update_user(message.chat.id, status=UserStatus.FREE)
		await client.send_message(message.chat.id, MESSAGES["main_menu"],
			reply_markup=USER_MENU)
#Kurslar
@Bot.on_message(filters.private & filters.regex(BTN_COURSES) &\
	(is_admin_free | (is_user_free & subscribed)))
async def show_courses(client, message):
	courses = [i.name for i in db.CATEGORY]
	if len(courses) == 0:
		await client.send_message(message.chat.id, MESSAGES["no_courses"])
		return
	courses = [courses[i:i+2] for i in range(0, len(courses), 2)]
	courses.append([BACK])
	if message.chat.id in ADMINS:
		db.update_admin(message.chat.id, status=UserStatus.SHOW_COURSES)
	else:
		db.update_user(message.chat.id, status=UserStatus.SHOW_COURSES)
	await client.send_message(message.chat.id, MESSAGES["show_courses"],
		reply_markup=ReplyKeyboardMarkup(courses, resize_keyboard=True))
#Bot haqida
@Bot.on_message(filters.private & (is_admin_free | (is_user_free & subscribed)) &\
	filters.regex(BTN_ABOUT))
async def about_bot(client, message):
	await client.send_message(message.chat.id, MESSAGES["about"])

