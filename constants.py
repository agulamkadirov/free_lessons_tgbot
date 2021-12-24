#Ba'zi kerakli constantalar saqlanadi
from pyrogram.types import ReplyKeyboardMarkup
import json

class MessageType:#Foydalanuvchiga yuboriladigan xabar turlari
	TEXT = 1
	PHOTO = 2
	VIDEO = 3
	FILE = 4

class UserStatus:
	FULL_NAME = -40
	AGE = -30
	GENDER = -20
	REGION = -10
	FREE = 0
	GET_NEW_CATEGORY = 10
	SHOW_COURSES = 20
	DEL_CATEGORY = 30
	SEND_LESSONS = 40
	GET_NEW_LESSONS = 50
	SEND_MESSAGE = 60

class UserTableCol:
	_id = 0
	tg_id = 1
	full_name = 2
	gender = 3
	age = 4
	region = 5
	last_message = 6
	status = 7

#menyular
BTN_COURSES = "Kurslar"
BTN_ADD_CATEGORY = "Kategoriya qo'shish"
BTN_SEND_MESSAGE = "Xabar yuborish"
BTN_STATISTIC = "Statistika"
BTN_ABOUT = "Bot haqida"
BTN_DEL_CATEGORY = "Kategoriya o'chirish"
ADMIN_MENU = ReplyKeyboardMarkup(
	[
		[BTN_COURSES, BTN_ADD_CATEGORY],
		[BTN_DEL_CATEGORY, BTN_SEND_MESSAGE],
		[BTN_STATISTIC, BTN_ABOUT]
	],
	resize_keyboard = True
)

USER_MENU = ReplyKeyboardMarkup(
	[
		[BTN_COURSES, BTN_ABOUT]
		# [BTN_ABOUT]
	],
	resize_keyboard = True
)

USER_GENDER = ReplyKeyboardMarkup(
	[
		["Erkak", "Ayol"]
	],
	resize_keyboard = True
)

USER_REGION = ReplyKeyboardMarkup(
	[
		["Qoraqalpog'iston Respublikasi"],
		["Andijon"],
		["Namangan"],
		["Farg'ona"],
		["Toshkent vil."],
		["Toshkent shahri"],
		['Sirdaryo'],
		["Jizzax"],
		["Samarqand"],
		["Buxoro"],
		["Xiva"],
		["Xorazm"],
		["Navoiy"],
		["Qashqadaryo"],
		["Surxondaryo"]
	],
	resize_keyboard = True
)

SENDING_MESSAGE_MENU = ReplyKeyboardMarkup(
	[
		["Yosh oraliqlari", "Hududlar"],
		["Jinsi","Tasdiqlash"],
		["Bekor qilish"]
	],
	resize_keyboard=True
)

MALE = "E"
FEMALE = "A"
BACK = "Ortga"
REGION = ["Qoraqalpog'iston Respublikasi", "Andijon",
		"Namangan", "Farg'ona", "Toshkent vil.",
		"Toshkent shahri", "Sirdaryo", "Jizzax",
		"Samarqand", "Buxoro", "Xiva", "Xorazm",
		"Navoiy", "Qashqadaryo", "Surxondaryo"]
MESSAGES = dict()
with open("messages.json", encoding="utf-8") as file:
	MESSAGES = json.loads(file.read())
