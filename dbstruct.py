from constants import REGION
import datetime

class User:
	def __init__(self, tg_id=0,
		gender="", age=0, region=0, last_message="", status=0):
		self.tg_id = tg_id
		self.gender = gender
		self.age = age
		if region is None:
			self.region = -1
		else:
			self.region = REGION[region]
		self.last_message = last_message
		self.status = status

class Admin:
	def __init__(self, tg_id=0, status=0, category_id=0):
		self.tg_id = tg_id
		self.status = status
		self.category_id = category_id

class Category:
	def __init__(self, id=0, name=""):
		self.id = id
		self.name = name

class Statistic:
	def __init__(self, user_count=0, karakalpak=0,
		andijan=0, namangan=0, ferghana=0, tashkent_reg=0,
		tashkent=0, syrdarya=0, jyzzakh=0, samarkand=0,
		bukhara=0, khiva=0, khorazm=0, navoiy=0, kashkadarya=0,
		surkhandarya=0):
		self.user_count = user_count
		self.karakalpak = karakalpak / user_count * 100
		self.andijan = andijan / user_count * 100
		self.namangan = namangan / user_count * 100
		self.ferghana = ferghana / user_count * 100
		self.tashkent_reg = tashkent_reg / user_count * 100
		self.tashkent = tashkent / user_count * 100
		self.syrdarya = syrdarya / user_count * 100
		self.jyzzakh = jyzzakh / user_count * 100
		self.samarkand = samarkand / user_count * 100
		self.bukhara = bukhara / user_count * 100
		self.khiva = khiva / user_count * 100
		self.khorazm = khorazm / user_count * 100
		self.navoiy = navoiy / user_count * 100
		self.kashkadarya = kashkadarya / user_count * 100
		self.surkhandarya = surkhandarya / user_count * 100

class AdminMessage:
	def __init__(self, id=None, created_at="", #min_age=0, max_age=0,
		sender_tg_id=0, message_id=0):
		self.id = id
		print(created_at, type(created_at))
		if type(created_at) == type(str()):
			self.created_at = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

		else:
			self.created_at = created_at
			print("datetime.datetime")

		self.sender_tg_id = sender_tg_id
		self.message_id = message_id