import asyncio
import logging


from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import Throttled


import config
from data_base import db
from view import View
from utils import parse_data


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

bot = Bot(token=config.BOT_TOKEN, loop=loop, parse_mode=types.ParseMode.MARKDOWN)
        

dp = Dispatcher(bot, storage=MemoryStorage())

view = View(bot)



@dp.callback_query_handler()
async def callback(callback):

    try:
        await dp.throttle('callback', rate = 0.8)

    except Throttled:
        await bot.answer_callback_query( callback.id, text = 'Флуд')
       

    else:
        await bot.answer_callback_query(callback.id)
        data = parse_data(callback.data)

        if data['action'] == 'open':
            getattr(view, data['action'])(callback.message)




@dp.message_handler(commands = ['start'])
async def start_command(msg):

    if await db.user_exist(user_id = msg.from_user.id):
        await view.main_menu(msg)
    
    else:
        # TODO: check referal here
        await db.create_user(user_id = msg.from_user)
        await view.welcome(msg)


@dp.message_handler()
async def text_hundler(msg):
    await view.main_menu(msg)


@dp.inline_handler()
async def inline_echo(inline_query):
    input_content = types.InputTextMessageContent(inline_query.query or 'echo')

    item = types.InlineQueryResultArticle(id='1', title='echo',
                                          input_message_content=input_content)

    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)



@dp.errors_handler()
async def error_hundler(msg, data):
    print(msg)
    print(data)
    # await bot.send_message('channel_info',str(msg))

 

executor.start_polling(dp, loop=loop, skip_updates=False)






