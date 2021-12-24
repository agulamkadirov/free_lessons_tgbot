import dbase_sqlite
import dbase_postgres

#postgresga sozlab qo'yamiz
# host = "localhost"
# user = "postgres"
# password = "postgres1361)"
host = "ec2-54-235-79-88.compute-1.amazonaws.com"
user = "otfosbntofyyvp"
password = "a2d976e612a8e2536c77044f93202864050b409eef297808b91d39e12093e0cc"

db = dbase_postgres.DBasePosgreSQL(host, "d9hi2kqi6cgsl8", user, password)

if __name__ == "__main__":
	# bu yerda bilganingni qil :)
	# message = db.get_message()
	# user = db.get_users("2021-12-12 11:11:11")
	db.insert_user(123)
	user = db.get_user(123)
	print(user.tg_id)
