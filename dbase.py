import dbase_sqlite
import dbase_postgres

#postgresga sozlab qo'yamiz
# host = "localhost"
# user = "postgres"
# password = "postgres1361)"
host = "ec2-54-145-139-208.compute-1.amazonaws.com"
user = "gbfdbpsguyeieu"
password = "6a0ea533355641bb1a987ba6462b5d1d507c45369c6e61b7704cea854051a2b5"

# db = dbase_postgres.DBasePosgreSQL(host, "ddg4uurarc0nui", user, password)
db = dbase_sqlite.DBase()

if __name__ == "__main__":
	# bu yerda bilganingni qil :)
	# message = db.get_message()
	# user = db.get_users("2021-12-12 11:11:11")
	db.insert_user(123)
	user = db.get_user(123)
	print(user.tg_id)
