from bot import Bot
from dbase import db
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton,\
	InlineKeyboardMarkup
from helper_functions import is_admin_free, asked_category_name,\
	asked_del_category_name, can_send_lessons, can_send_category_name,\
	can_get_lessons, can_set_age, can_send_message
from constants import UserStatus, MESSAGES, BACK, BTN_ADD_CATEGORY,\
	ADMIN_MENU, UserStatus, BTN_DEL_CATEGORY, SENDING_MESSAGE_MENU,\
	BTN_SEND_MESSAGE, BTN_STATISTIC
#Kategoriya qo'shish
@Bot.on_message(filters.private & is_admin_free & filters.regex(BTN_ADD_CATEGORY))
async def ask_category_name(client, message):
	db.update_admin(message.chat.id, status=UserStatus.GET_NEW_CATEGORY)
	await client.send_message(message.chat.id, MESSAGES["ask_category_name"],
		reply_markup=ReplyKeyboardMarkup([[BACK]], resize_keyboard=True))
#Kategoriya muvaffaqqiyatli qo'shildi
@Bot.on_message(filters.private & asked_category_name & filters.text & can_send_category_name)
async def get_category_name(client, message):
	db.insert_category(message.text)
	db.update_admin(message.chat.id, status=UserStatus.FREE)
	await client.send_message(message.chat.id,
		MESSAGES["successfully_category_created"], reply_markup=ADMIN_MENU)
#Kategoriya o'chirish
@Bot.on_message(filters.private & is_admin_free & filters.regex(BTN_DEL_CATEGORY))
async def choose__category_name(client, message):
	courses = [i.name for i in db.CATEGORY]
	if len(courses) == 0:
		await client.send_message(message.chat.id, MESSAGES["no_courses"])
		return
	db.update_admin(message.chat.id, status=UserStatus.DEL_CATEGORY)
	courses = [courses[i:i+2] for i in range(0, len(courses), 2)]
	courses.append([BACK])
	await client.send_message(message.chat.id, MESSAGES["del_category_name"],
		reply_markup=ReplyKeyboardMarkup(courses, resize_keyboard=True))
#Tanlangan kategoriyani o'chirish
@Bot.on_message(filters.private & asked_del_category_name)
async def confirm_del_category(client, message):
	for i in db.CATEGORY:
		if i.name == message.text:
			#TODO kategoriya o'chirishni tasdiqlashni qo'shish
			db.del_category(i.id)
			await client.send_message(message.chat.id, MESSAGES["success"],
				reply_markup=ADMIN_MENU)
			db.update_admin(message.chat.id, status=UserStatus.FREE)
			# del db.[db.index(i)]
			break
#Admin.status==SHOW_COURSES bo'lib kurs tanlanganda
@Bot.on_message(filters.private & can_send_lessons)
async def send_category_lessons(client, message):
	for i in db.CATEGORY:
		if i.name == message.text:
			db.update_admin(message.chat.id, category_id=i.id,
				status=UserStatus.SEND_LESSONS)
			await client.send_message(message.chat.id,
				MESSAGES["send_lessons"], reply_markup=ReplyKeyboardMarkup([[BACK]],
					resize_keyboard=True))
#Admin kurs tanlab darslik jo'natganda
@Bot.on_message(filters.private & can_get_lessons)
async def get_new_lesson(client, message):
	admin = db.get_admin(message.chat.id)
	db.insert_lesson(message.chat.id, message.message_id)
	await client.send_message(message.chat.id, MESSAGES["saved_lesson"],
		reply_markup=ReplyKeyboardMarkup([[BACK]], resize_keyboard=True))
#Admin xabar jo'natish ni tanlagandan:
@Bot.on_message(filters.private & is_admin_free & filters.regex(BTN_SEND_MESSAGE))
async def ask_message(client, message):
	db.update_admin(message.chat.id, status=UserStatus.SEND_MESSAGE)
	# db.create_message(message.chat.id)
	await client.send_message(message.chat.id, MESSAGES["ask_to_send_message"],
		reply_markup=ReplyKeyboardMarkup([[BACK]], resize_keyboard=True))
#Admin xabar jo'natishni bosib xabar yozganda:
@Bot.on_message(filters.private & can_send_message)
async def get_message(client, message):
	# db.update_message(message.chat.id, completed=1, message_id=message.message_id)
	db.create_message(message.chat.id, message.message_id)
	db.update_admin(message.chat.id, status=UserStatus.FREE)
	await client.send_message(message.chat.id, MESSAGES["success"],
		reply_markup=ADMIN_MENU)
	await client.send_message_to_users()
#Statistika
@Bot.on_message(filters.private & is_admin_free & filters.regex(BTN_STATISTIC))
async def show_statistic(client, message):
	statistic = db.get_statistic()
	text = f"""Botdan foydalanayotganlar soni: <b>{statistic.user_count:,}</b>
	Ulardan:

	<b>Qoraqalpog'iston Respublikasi</b>: {round(statistic.karakalpak, 2)}%
	<b>Andijon</b>: {round(statistic.andijan, 2)}%
	<b>Namangan</b>: {round(statistic.namangan, 2)}%
	<b>Farg'ona</b>: {round(statistic.ferghana, 2)}%
	<b>Toshkent vil.</b>: {round(statistic.tashkent_reg, 2)}%
	<b>Toshkent sh.</b>: {round(statistic.tashkent, 2)}%
	<b>Sirdaryo</b>: {round(statistic.syrdarya, 2)}%
	<b>Jizzax</b>: {round(statistic.jyzzakh, 2)}%
	<b>Samarqand</b>: {round(statistic.samarkand, 2)}%
	<b>Buxoro</b>: {round(statistic.bukhara, 2)}%
	<b>Xiva</b>: {round(statistic.khiva, 2)}%
	<b>Xorazm</b>: {round(statistic.khorazm, 2)}%
	<b>Navoiy</b>: {round(statistic.navoiy, 2)}%
	<b>Qashqadaryo</b>: {round(statistic.kashkadarya, 2)}%
	<b>Surxondaryo</b>: {round(statistic.surkhandarya, 2)}%
	"""

	await client.send_message(message.chat.id, text);