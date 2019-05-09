import asyncio
import logging


from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import Throttled


import config


from utils import parse_data


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

bot = Bot(token=config.BOT_TOKEN, loop=loop, parse_mode=types.ParseMode.MARKDOWN)
        

dp = Dispatcher(bot, storage=MemoryStorage())
def run():
  from hundlers import init
  init(bot, dp)

if __name__ == '__main__':
  run()  

executor.start_polling(dp, loop=loop, skip_updates=False)
