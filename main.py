from bot import Bot

from traceback import format_exc

with open('token.txt') as fin:
    TOKEN = fin.read().strip()

bot = Bot(TOKEN, "./emias_buff.csv")

try:
    bot.loop()
except:
    traceback = format_exc()
    print(traceback)
    bot.send_error_alert(traceback)