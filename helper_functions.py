
#filterlar bor asosan
from config import ADMINS, CHANNEL_ID
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait
from dbase import db
from constants import UserStatus, REGION, BACK

async def is_subscribed(filter, client, update):
	if CHANNEL_ID == 0:
		return True
	user_id = update.from_user.id
	if user_id in ADMINS:
		return True
	try:
		member = await client.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
	except UserNotParticipant:
		return False
	if not member.status in ["creator", "administrator", "member"]:
		return False
	else:
		return True

async def check_for_subscription(_, __, query):
	return query.data == "check_subscription"

async def get_full_name(filter, client, message):
	user = db.get_user(message.chat.id)
	data = message.text.split()
	return user is not None and user.status == UserStatus.FULL_NAME and len(data) == 2 and data[0].isalpha() and data[1].isalpha()

async def get_age(filter, client, message):
	user = db.get_user(message.chat.id)
	data = message.text
	return user is not None and user.status == UserStatus.AGE and data.isdigit() and 7<=int(data)<=100

async def get_gender(filter, client, message):
	user = db.get_user(message.chat.id)
	data = message.text
	return user is not None and user.status == UserStatus.GENDER and data in ["Erkak", "Ayol"]

async def get_region(filter, client, message):
	user = db.get_user(message.chat.id)
	data = message.text
	return user is not None and user.status == UserStatus.REGION and data in REGION

async def get_new_category(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin.status == UserStatus.GET_NEW_CATEGORY

async def _is_user_free(filter, client, message):
	user = db.get_user(message.chat.id)
	return user is not None and user.status == UserStatus.FREE

async def _is_admin_free(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.FREE

async def get_new_category_name(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.GET_NEW_CATEGORY

async def choose_del_category_name(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.DEL_CATEGORY and\
	message.text in [i.name for i in db.CATEGORY]

async def send_lessons(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.SHOW_COURSES and\
	message.text in [i.name for i in db.CATEGORY]

async def _can_send_category_name(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.GET_NEW_CATEGORY and\
	message.text != BACK

async def _get_lessons(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.SEND_LESSONS and\
	message.text != BACK

async def user_get_lessons(filter, client, message):
	user = db.get_user(message.chat.id)
	if user is None:
		user = db.get_admin(message.chat.id)
		if user is None:
			return False
	return user.status == UserStatus.SHOW_COURSES and\
	message.text in [i.name for i in db.CATEGORY]

async def _can_set_age(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.SEND_MESSAGE and\
	message.text == "Yosh oraliqlari"

async def _can_send_message(filter, client, message):
	admin = db.get_admin(message.chat.id)
	return admin is not None and admin.status == UserStatus.SEND_MESSAGE and\
	message.text != "Ortga"

subscribed = filters.create(is_subscribed)
check_subscription = filters.create(check_for_subscription)
asked_full_name = filters.create(get_full_name)
asked_age = filters.create(get_age)
asked_gender = filters.create(get_gender)
asked_region = filters.create(get_region)
add_new_category = filters.create(get_new_category)
is_user_free = filters.create(_is_user_free)
is_admin_free = filters.create(_is_admin_free)
asked_category_name = filters.create(get_new_category_name)
asked_del_category_name = filters.create(choose_del_category_name)
can_send_lessons = filters.create(send_lessons)
can_send_category_name = filters.create(_can_send_category_name)
can_get_lessons = filters.create(_get_lessons)
can_user_get_lessons = filters.create(user_get_lessons)
can_set_age = filters.create(_can_set_age)
can_send_message = filters.create(_can_send_message)
