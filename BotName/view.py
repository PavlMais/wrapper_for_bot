from aiogram.types import  InlineKeyboardMarkup as Markup
from aiogram.types import  InlineKeyboardButton as Button

from aiogram.utils.exceptions import MessageToEditNotFound, MessageCantBeEdited
from .msgids import msgids

from .data_base import db
from . import config
from main import bot

class View(object):

    def edit(func):
        async def decor(self, msg, *args, **kwargs):
        
            if msg.from_user.id != config.BOT_ID: # if user send msg delete 
                await self.bot.delete_message(msg.chat.id, msg.message_id)
            
           
            text, buttons = await func(self, *args, **kwargs)
        
            try:
                await self.bot.edit_message_text(
                    chat_id = msg.chat.id,
                    message_id = await msgids.get(msg.chat.id),
                    text = text,
                    reply_markup = buttons
                )
            except (MessageToEditNotFound, MessageCantBeEdited) as e:
                print('MessageToEditNotFound: ', e)

                s_msg = await self.bot.send_message(msg.chat.id, text, reply_markup = buttons)

                await msgids.add(msg.chat.id, s_msg.message_id)

            except Exception as e:
                print('Error edit msg: ', e)
    
        return decor



    @edit
    async def main_menu(self):
        return 'Main menu', None

    @edit
    async def welcome(self):
        btn = Markup().add(
            Button('OK', callback_data='open main_menu')
        )
        return 'Welcome menu', btn
    
    
    
view = View()
