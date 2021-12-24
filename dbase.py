import dbase_sqlite
import dbase_postgres

#postgresga sozlab qo'yamiz
# host = "localhost"
# user = "postgres"
# password = "postgres1361)"
host = "ec2-54-173-2-216.compute-1.amazonaws.com"
user = "mimeqpehadcsda"
password = "aa737a7300c03a912a966df366a2f1a3f9badfe64537b3dfdcb0a1c0eaeeb279"

db = dbase_postgres.DBasePosgreSQL(host, "dbmktco47qknho", user, password)

if __name__ == "__main__":
	# bu yerda bilganingni qil :)
	# message = db.get_message()
	# user = db.get_users("2021-12-12 11:11:11")
	db.insert_user(123)
	user = db.get_user(123)
	print(user.tg_id)
