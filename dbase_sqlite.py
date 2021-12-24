#sqlite3 bilan ishlash uchun
import sqlite3
from config import DBASE_PATH, ADMINS
from constants import UserStatus, REGION
import datetime
# from constants import UserStatus, UserTableCol
from dbstruct import *

class DBase:
	def __init__(self):
		self.connection = sqlite3.connect(DBASE_PATH)
		self.cursor = self.connection.cursor()
		self.CATEGORY = []
		self.cursor.execute("SELECT * FROM Category;")
		for i in self.cursor:
			self.CATEGORY.append(Category(*i))

	def __del__(self):
		self.connection.close()
	def insert_user(self, tg_id):
		#Kanalga a'zo bo'gach, start bosganda db ga foydalanuvchi qo'shiladi
		#User Status qaytariladi
		user = self.get_user(tg_id)
		if user is None:
			self.cursor.execute(f"INSERT INTO User(tg_id, status) VALUES({tg_id}, {UserStatus.AGE});")
			self.connection.commit()
			return UserStatus.AGE
		return user.status

	def update_user(self, tg_id, **kwargs):
		command = "UPDATE User SET "
		for key, value in kwargs.items():
			command += key + "='" + str(value) + "',"
		command = command[:-1] + f" WHERE tg_id={tg_id};"
		self.cursor.execute(command)
		self.connection.commit()

	def get_user(self, tg_id):
		self.cursor.execute(f"SELECT * FROM User WHERE tg_id={tg_id};")
		data = self.cursor.fetchone()
		if data is None:
			return None
		return User(*data)
	def insert_admin(self, tg_id):
		self.cursor.execute(f"SELECT * FROM Admin WHERE tg_id={tg_id};")
		data = self.cursor.fetchone()
		if data is None:
			self.cursor.execute(f"INSERT INTO Admin(tg_id) VALUES({tg_id});")
			self.connection.commit()
	def update_admin(self, tg_id, **kwargs):
		if tg_id not in ADMINS:
			self.insert_admin(tg_id)
		command = "UPDATE Admin SET "
		for key, value in kwargs.items():
			command += key + "='" + str(value) + "',"
		command = command[:-1] + f" WHERE tg_id={tg_id};"
		self.cursor.execute(command)
		self.connection.commit()
	def get_admin(self, tg_id):
		self.cursor.execute(f"SELECT * FROM Admin WHERE tg_id={tg_id};")
		data = self.cursor.fetchone()
		if data is None:
			return None
		return Admin(*data)
	def insert_category(self, category_name=""):
		self.cursor.execute(f"INSERT INTO Category(name) VALUES(\"{category_name}\");")
		self.connection.commit()
		self.cursor.execute(f"SELECT * FROM Category WHERE name=\"{category_name}\";")
		self.CATEGORY.append(Category(*self.cursor.fetchone()))
	def del_category(self, category_id=0):
		self.cursor.execute(f"DELETE FROM Lessons WHERE category_id={category_id};")
		self.connection.commit()
		self.cursor.execute(f"DELETE FROM Category WHERE id={category_id};")
		self.connection.commit()
		for i in range(len(self.CATEGORY)):
				if self.CATEGORY[i].id == category_id:
					del self.CATEGORY[i]
					break
	def get_statistic(self):
		self.cursor.execute("""SELECT COUNT(*), COUNT(case when region==0 then 1 end),
			COUNT(case when region==1 then 1 end), COUNT(case when region==2 then 1 end),
			COUNT(case when region==3 then 1 end), COUNT(case when region==4 then 1 end),
			COUNT(case when region==5 then 1 end), COUNT(case when region==6 then 1 end),
			COUNT(case when region==7 then 1 end), COUNT(case when region==8 then 1 end),
			COUNT(case when region==9 then 1 end), COUNT(case when region==10 then 1 end),
			COUNT(case when region==11 then 1 end), COUNT(case when region==12 then 1 end),
			COUNT(case when region==13 then 1 end) FROM User;""")
		return Statistic(*self.cursor.fetchone())
	def insert_lesson(self, sender_tg_id=0, message_id=0):
		sender = self.get_admin(sender_tg_id)
		self.cursor.execute(f"INSERT INTO Lessons(category_id, chat_id, message_id) \
			VALUES({sender.category_id}, {sender_tg_id}, {message_id});")
		self.connection.commit()
	def get_lessons(self, category_id=0):
		self.cursor.execute(f"SELECT * FROM Lessons WHERE category_id={category_id};")
		return self.cursor
	def create_message(self, sender_tg_id=0, message_id=0):
		self.cursor.execute(f"INSERT INTO Message(sender_tg_id, created_at, message_id, completed) VALUES({sender_tg_id}, \"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\",{message_id},1)")
		self.connection.commit()
	def update_message(self, sender_tg_id, **kwargs):
		command = "UPDATE Message SET "
		for key, value in kwargs.items():
			command += key + "='" + str(value) + "',"
		command = command[:-1] + f" WHERE sender_tg_id={sender_tg_id};"
		self.cursor.execute(command)
		self.connection.commit()
	def get_message(self):
		cursor = self.cursor.execute(f"SELECT * FROM Message LIMIT 1")
		data = cursor.fetchone()
		if data is None:
			return None
		return AdminMessage(*data)
	def get_users(self, last_message=""):
		cursor = self.cursor.execute(f"SELECT tg_id FROM User WHERE last_message!=\"{last_message}\";")
		return cursor
	def delete_message(self, id):
		self.cursor.execute(f"DELETE FROM Message WHERE id={id};")
		self.connection.commit()

