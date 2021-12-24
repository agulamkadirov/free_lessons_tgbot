#botga start bosganda
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton,\
	ReplyKeyboardMarkup
from bot import Bot
from dbase import db
from constants import UserStatus, MESSAGES, ADMIN_MENU, USER_MENU,\
	 MALE, FEMALE, REGION, USER_REGION
from helper_functions import subscribed, check_subscription, asked_full_name,\
	asked_age, asked_gender, asked_region
from config import INVITE_LINK, ADMINS

@Bot.on_message(filters.command("start") & filters.private & subscribed)
async def start_command(client, message):
	if message.chat.id in ADMINS:
		db.update_admin(message.chat.id, status=UserStatus.FREE)
		await client.send_message(message.chat.id, MESSAGES["admin_started"],
			reply_markup=ADMIN_MENU)
		return
	user_status = db.insert_user(message.chat.id)	#Foydalanuvchi statusiga ko'ra yo'naltiriladi
	print(user_status)
	if user_status == UserStatus.FULL_NAME:
		await client.send_message(message.chat.id, MESSAGES["ask_full_name"])
	elif user_status == UserStatus.AGE:
		await client.send_message(message.chat.id, MESSAGES["ask_age"])
	elif user_status == UserStatus.GENDER:
		await client.send_message(message.chat.id, MESSAGES["ask_gender"],
			reply_markup=ReplyKeyboardMarkup([["Erkak", "Ayol"]], resize_keyboard=True))
	elif user_status == UserStatus.REGION:
		await client.send_message(message.chat.id, MESSAGES["ask_region"],
			reply_markup=USER_REGION)
	else:
		await client.send_message(message.chat.id, MESSAGES["welcome_back"],
			reply_markup=USER_MENU)

@Bot.on_message(filters.command("start") & filters.private)
async def go_and_subscribe(client, message):
	if message.chat.id in ADMINS:
		await client.send_message(message.chat.id, MESSAGES["admin_started"], reply_markup=ADMIN_MENU)
		return
	await message.reply(text=MESSAGES["not_subscribed"],
		reply_markup=InlineKeyboardMarkup([
				[
					InlineKeyboardButton(text="Kanalga qo'shilish", url=INVITE_LINK)
				],
				[
					InlineKeyboardButton(text="Tekshirish", callback_data="check_subscription")
				]
			]))

@Bot.on_callback_query(check_subscription)
async def _check_subscription(client, query):
	if await subscribed(client, query):
		try:
			await client.delete_messages(query.from_user.id, query.message.message_id)
		except Exception as e:
			print(e)
		await start_command(client, query.message)
	else:
		await client.answer_callback_query(query.id, "Avval ko'rsatilgan kanalga o'ting!")

@Bot.on_message(filters.private & subscribed & asked_full_name)
async def _get_full_name(client, message):
	db.update_user(message.chat.id, full_name=message.text, status=UserStatus.AGE)
	await client.send_message(message.chat.id, MESSAGES["ask_age"])

@Bot.on_message(filters.private & subscribed & asked_age)
async def _get_age(client, message):
	db.update_user(message.chat.id, age=message.text, status=UserStatus.GENDER)
	await client.send_message(message.chat.id, MESSAGES["ask_gender"],
		reply_markup=ReplyKeyboardMarkup([["Erkak", "Ayol"]], resize_keyboard=True))

@Bot.on_message(filters.private & subscribed & asked_gender)
async def _get_gender(client, message):
	if message.text == "Erkak":
		message.text = MALE
	else:
		message.text = FEMALE
	db.update_user(message.chat.id, gender=message.text, status=UserStatus.REGION)
	await client.send_message(message.chat.id, MESSAGES["ask_region"], reply_markup=USER_REGION)

@Bot.on_message(filters.private & subscribed & asked_region)
async def _get_region(client, message):
	data = REGION.index(message.text)
	db.update_user(message.chat.id, region=data, status=UserStatus.FREE)
	await client.send_message(message.chat.id, MESSAGES["welcome"], reply_markup=USER_MENU)
