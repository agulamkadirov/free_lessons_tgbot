
from bot import Bot
from dbase import db
import asyncio

app = Bot()
app.run(app.send_message_to_users())
app.run()

# if __name__ == "__main__":
	
# 	async def bot_run():
# 		app = await Bot.create_object()
# 		app.run()

# 	asyncio.run(bot_run())
	

