# -*- coding: utf-8 -*-
"""
Project: matrix-pybot

"""
# Examle for an event (type: m.room.message), taken from the matrix.org spec:
# {
#    "sender": "@alice:example.com",
#    "type": "m.room.message",
#    "txn_id": "1234",
#    "content": {
#       "body": "I am a fish",
#       "msgtype": "m.text"
#    },
#    "origin_server_ts": 1417731086797,
#    "event_id": "$74686972643033:example.com"
# }

import logging
import re

from matrix_client.client import MatrixClient
from matrix_client.errors import MatrixRequestError


__version__ = '0.1'
__license__ = 'MIT'
__author__ = 'Thorsten Weimann <@Thorsten:whitie.ddns.net>'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class BaseHandler:

    def __init__(self, test_func, callback):
        self.should_run = test_func
        self.callback = callback

    def __call__(self, room, event):
        logger.info('Calling handler function: %s', self.callback.__name__)
        logger.debug('Room: %s', room)
        logger.debug('Event: %s', event)
        return self.callback(room, event)


class RegexHandler(BaseHandler):

    def __init__(self, regex_string, callback, re_flags=0):
        BaseHandler.__init__(self, self.should_process, callback)
        self.regex = re.compile(regex_string, re_flags)

    def should_process(self, room, event):
        if event['type'] == 'm.room.message':
            return bool(self.regex.search(event['content']['body']))
        return False


class CommandHandler(RegexHandler):
    vorbidden = '@#+'

    def __init__(self, command, callback, cmd_init='!'):
        if cmd_init in self.vorbidden:
            raise ValueError(
                '"{}" not allowed as cmd init character'.format(self.vorbidden)
            )
        cmd = '{}{}'.format(re.escape(cmd_init), command)
        # Commands should not be case sensitive
        RegexHandler.__init__(self, cmd, callback, re.IGNORECASE)


class MatrixBot:

    def __init__(self, username, password, server, allowed_rooms=None):
        self.username = username
        self._username_re = re.compile('@{}'.format(re.escape(username)), re.I)
        self.server = server
        self.handlers = []
        self.rooms = {}
        self.client = MatrixClient(server)
        try:
            self.client.login_with_password(username, password)
        except MatrixRequestError as error:
            if error.code == 403:
                logger.error('Username and/or password mismatch')
            raise
        self._join_rooms(allowed_rooms)
        if not self.rooms:
            logger.info('No rooms given, listening for invitations')
            self.client.add_invite_listener(self.handle_invite)
            for room_id, room in self.client.rooms.items():
                room.add_listener(self.handle_message)
                self._add_room(room_id, room)

    def _add_room(self, room_id, room):
        logger.debug('Adding room (ID: %s): %s', room_id, room)
        self.rooms[room_id] = room

    def _join_rooms(self, room_ids):
        for room_id in room_ids:
            room = self.client.join_room(room_id)
            room.add_listener(self.handle_message)
            self._add_room(room_id, room)

    def send(self, msg, room_ids=None):
        rooms = room_ids or self.rooms.keys()
        for room_id in rooms:
            room = self.rooms.get(room_id)
            if room:
                room.send_text(msg)

    def handle_message(self, room, event):
        if self._username_re.match(event['sender']):
            # Don't handle own messages
            return
        for handler in self.handlers:
            assert isinstance(handler, BaseHandler)
            if handler.should_run(room, event):
                try:
                    handler(room, event)
                except Exception:
                    logger.exception('Error while calling handler function')

    def handle_invite(self, room_id, state):
        logger.info('Invitation received to: %s', room_id)
        logger.info('Trying to join now...')
        room = self.client.join_room(room_id)
        room.add_listener(self.handle_message)
        self.rooms[room_id] = room

    def start(self):
        """Starts listening for messages in a new thread. If the calling
        script has nothing more to do, it can simply do:
        >>> bot = MatrixBot(username, password, server, allowed_rooms)
        >>> bot_thread = bot.start()
        >>> bot_thread.join()
        This will run forever.
        """
        self.client.start_listener_thread()
        return self.client.sync_thread

    def stop(self):
        self.client.stop_listener_thread()
