from data_base import db
import config

class MsgIDS(object):

    def __init__(self):
        self._msg_ids = {}

    async def add(self, user_id, msg_id):

        self._msg_ids[user_id] = msg_id
        
        await db.set_msg_id(user_id = user_id, msg_id = msg_id)

        if len(self._msg_ids) > config.SIZE_BUFFER_MSGS_IDS:
            del self._msg_ids[list(self._msg_ids.keys())[0]]


    async def get(self, user_id):

        msg_id = self._msg_ids.get(user_id)

        if msg_id is None:
            msg_id = await db.get_msg_id(user_id = user_id)

        return msg_id


msgids = MsgIDS()