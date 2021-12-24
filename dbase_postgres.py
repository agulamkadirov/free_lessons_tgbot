#postgresql bilan ishlash uchun
from dbstruct import *
import psycopg2
from config import DBASE_PATH, ADMINS
from constants import UserStatus, REGION
import datetime

class DBasePosgreSQL:
	def __init__(self, host, database, user, password):
		self.connection = psycopg2.connect(host=host,
			database=database,
			user=user,
			password=password)
		self.cursor = self.connection.cursor()
		self.CATEGORY = []
		try:
			self.cursor.execute('SELECT * FROM "Category";')
			for i in self.cursor:
				self.CATEGORY.append(Category(*i))
		except Exception as e:
			print(e)
			self.connection.rollback()

	def __del__(self):
		print("Tugadi :)")
		self.connection.close()

	def insert_user(self, tg_id):
		#Kanalga a'zo bo'gach, start bosganda db ga foydalanuvchi qo'shiladi
		#User Status qaytariladi
		user = self.get_user(tg_id)
		if user is None:
			try:
				x = str(datetime.datetime.now())
				x = x[:x.find(".")]
				self.cursor.execute(f'INSERT INTO public."User"(tg_id, status, last_message) VALUES({tg_id}, {UserStatus.AGE},\'{x}\');')
				self.connection.commit()
				return UserStatus.AGE
			except Exception as e:
				print(e)
				self.connection.rollback()
				return None

		return user.status

	def update_user(self, tg_id, **kwargs):
		command = 'UPDATE public."User" SET '
		for key, value in kwargs.items():
			command += key + "='" + str(value) + "',"
		command = command[:-1] + f" WHERE tg_id={tg_id};"
		try:
			self.cursor.execute(command)
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()

	def get_user(self, tg_id):
		try:
			self.cursor.execute(f'SELECT * FROM public."User" WHERE tg_id={tg_id};')
		except Exception as e:
			print(e)
			self.connection.rollback()
			return

		data = self.cursor.fetchone()
		if data is None:
			return None
		return User(*data)

	def insert_admin(self, tg_id):
		try:
			self.cursor.execute(f'SELECT * FROM public."Admin" WHERE tg_id={tg_id};')
		except Exception as e:
			print(e)
			self.connection.rollback()
			return

		data = self.cursor.fetchone()
		if data is None:
			try:
				self.cursor.execute(f'INSERT INTO public."Admin"(tg_id) VALUES({tg_id});')
				self.connection.commit()
			except Exception as e:
				print(e)
				self.connection.rollback()

	def update_admin(self, tg_id, **kwargs):
		if tg_id not in ADMINS:
			self.insert_admin(tg_id)
		command = 'UPDATE public."Admin" SET '
		for key, value in kwargs.items():
			command += key + "='" + str(value) + "',"
		command = command[:-1] + f" WHERE tg_id={tg_id};"
		try:
			self.cursor.execute(command)
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()
			db.insert_admin(tg_id)

	def get_admin(self, tg_id):
		try:
			self.cursor.execute(f'SELECT * FROM public."Admin" WHERE tg_id={tg_id};')
		except Exception as e:
			print(3)
			self.connection.rollback()
			return

		data = self.cursor.fetchone()
		if data is None:
			return None
		return Admin(*data)

	def insert_category(self, category_name=""):
		try:
			self.cursor.execute(f'INSERT INTO public."Category"(name) VALUES(\'{category_name}\');')
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()
			return

		try:
			self.cursor.execute(f'SELECT * FROM public."Category" WHERE name=\'{category_name}\';')
			self.CATEGORY.append(Category(*self.cursor.fetchone()))
		except Exception as e:
			print(e)
			self.connection.rollback()

	def del_category(self, category_id=0):
		try:
			self.cursor.execute(f'DELETE FROM public."Lessons" WHERE category_id={category_id};')
			self.connection.commit()
			for i in range(len(self.CATEGORY)):
				if self.CATEGORY[i].id == category_id:
					del self.CATEGORY[i]
					break
		except Exception as e:
			print(e)
			self.connection.rollback()
			return

		try:
			self.cursor.execute(f'DELETE FROM public."Category" WHERE id={category_id};')
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()

	def get_statistic(self):
		try:
			self.cursor.execute("""SELECT COUNT(*), COUNT(case when region=0 then 1 end),
				COUNT(case when region=1 then 1 end), COUNT(case when region=2 then 1 end),
				COUNT(case when region=3 then 1 end), COUNT(case when region=4 then 1 end),
				COUNT(case when region=5 then 1 end), COUNT(case when region=6 then 1 end),
				COUNT(case when region=7 then 1 end), COUNT(case when region=8 then 1 end),
				COUNT(case when region=9 then 1 end), COUNT(case when region=10 then 1 end),
				COUNT(case when region=11 then 1 end), COUNT(case when region=12 then 1 end),
				COUNT(case when region=13 then 1 end) FROM public."User";""")
		except Exception as e:
			print(e)
			self.connection.rollback()
			return Statistic()

		return Statistic(*self.cursor.fetchone())

	def insert_lesson(self, sender_tg_id=0, message_id=0):
		sender = self.get_admin(sender_tg_id)
		try:
			self.cursor.execute(f'INSERT INTO public."Lessons"(category_id, chat_id, message_id) \
				VALUES({sender.category_id}, {sender_tg_id}, {message_id});')
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()

	def get_lessons(self, category_id=0):
		try:
			self.cursor.execute(f'SELECT * FROM public."Lessons" WHERE category_id={category_id};')
			return self.cursor
		except Exception as e:
			print(e)
			self.connection.rollback()

	def create_message(self, sender_tg_id=0, message_id=0):
		try:
			self.cursor.execute(f'INSERT INTO public."Message"(created_at, sender_tg_id, message_id) VALUES(\'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\',{sender_tg_id},{message_id})')
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()

	def update_message(self, sender_tg_id, **kwargs):
		command = 'UPDATE public."Message" SET '
		for key, value in kwargs.items():
			command += key + "='" + str(value) + "',"
		command = command[:-1] + f" WHERE sender_tg_id={sender_tg_id};"
		try:
			self.cursor.execute(command)
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()

	def get_message(self):
		try:
			self.cursor.execute(f'SELECT * FROM public."Message" LIMIT 1;')
		except Exception as e:
			print(e)
			self.connection.rollback()
			return

		data = self.cursor.fetchone()
		if data is None:
			return None
		print(data)
		return AdminMessage(*data)

	def get_users(self, last_message=""):
		try:
			self.cursor.execute(f'SELECT tg_id FROM public."User" WHERE last_message!=\'{last_message}\';')
		except Exception as e:
			print(e)
			self.connection.rollback()
			return None
		return self.cursor.fetchall()

	def delete_message(self, id):
		try:
			self.cursor.execute(f'DELETE FROM public."Message" WHERE id={id};')
			self.connection.commit()
		except Exception as e:
			print(e)
			self.connection.rollback()


