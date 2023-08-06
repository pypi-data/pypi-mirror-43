import logging

from channels.generic.http import AsyncHttpConsumer
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer

name = "bluesocket"

logger = logging.getLogger()


class Logger(logging.Logger):
    def __init__(self, consumer, name, level=logging.NOTSET,
                 log_level_key='log'):
        super(DjangoAdapter, self).__init__(name=name, level=level)
        self.consumer = consumer
        self.consumer_name = consumer.__name__
        self.log_level_key = log_level_key

    def _get_log_level_by_dict(self, level, msg):
        log_level = level._levelToName[level]
        if type(msg) != dict:
            raise ValueError('msg parameter must be a dictionary')
        if type(log_level) != str:
            raise ValueError('level parameter must be a string')
        msg[self.log_level_key] = log_level
        return msg

    def _get_log_level_by_text(self, level, text):
        log_level = level._levelToName[level]
        if type(text) != str:
            raise ValueError('msg parameter must be a string')
        log_msg = f"{log_level}: {text}"
        return log_msg

    def _log(self, level, msg, args, exc_info=None, extra=None,
             stack_info=False):
        if isinstance(self.consumer, WebsocketConsumer):
            msg = self._get_log_level_by_text(level, msg)
            self.consumer.send(text_data=msg)
            return
        if isinstance(self.consumer, JsonWebsocketConsumer) or isinstance(
                self.consumer, AsyncJsonWebsocketConsumer):
            msg = self._get_log_level_by_dict(level, msg)
            self.consumer.send_json(msg)
            return
    