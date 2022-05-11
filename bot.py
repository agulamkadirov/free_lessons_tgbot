from pyrogram import Client
from config import API_ID, API_HASH, ADMINS, TOKEN
from dbase import db
import asyncio
from config import ADMINS

class Bot(Client):
	def __init__(self):
		super().__init__(
				"Bot",
				api_hash = API_HASH,
				api_id = API_ID,
				plugins={
                "root": "plugins"
            	},
				bot_token = TOKEN
			)
		self.sending_message = False
		# self.send_message_to_users()

	async def send_message_to_users(self):
		if self.sending_message:
			return
		message = db.get_message()
		if message is not None: print("Sending...", message, message.created_at)

		self.sending_message = True
		try:
			async with self:
				while message is not None:
					cursor = db.get_users(message.created_at)
					for tg_id in cursor:
						try:
							await self.copy_message(tg_id[0], from_chat_id=message.sender_tg_id,
								message_id=message.message_id)
						except Exception as e:
							print(e)

						db.update_user(tg_id[0], last_message=message.created_at)
						await asyncio.sleep(5)
					db.delete_message(message.id)
					message = db.get_message()
		except Exception as e:
			while message is not None:
				cursor = db.get_users(message.created_at)
				for tg_id in cursor:
					print(tg_id)
					await self.copy_message(tg_id[0], from_chat_id=message.sender_tg_id,
						message_id=message.message_id)
					db.update_user(tg_id[0], last_message=message.created_at)
					await asyncio.sleep(5);
				db.delete_message(message.id)
				message = db.get_message()

		print("While tugadi")
		for i in ADMINS:
			db.insert_admin(i)
		self.sending_message = False

	@classmethod
	async def create_object(cls):
		self = Bot()
		# await self.send_message_to_users()
		return self
