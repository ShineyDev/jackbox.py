"""
/jackbox/_wss.py

    Copyright (c) 2020 ShineyDev
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import asyncio
import json
import random

import websockets

from jackbox.objects import _PLAYER_TYPE_MAP
from jackbox.objects.blobs import _BLOB_TYPE_MAP


_WS_URI = "wss://{0}:38203/socket.io/1/websocket/{1}"

_WS_EVENT_KEY_MAP = {
    "Event": "event",
    "Result": "action",
}

_WS_EVENT_MAP = {
    "CustomerBlobChanged": "customer_blob_changed",
    "JoinRoom": "room_join",
    "RoomBlobChanged": "room_blob_changed",
    "RoomDestroyed": "room_destroy",
}

_START_COUNTDOWN_MAP = {

}

_CANCEL_COUNTDOWN_MAP = {

}


def _build_message(type, data=None):
    if data is not None:
        data = json.dumps(data, separators=(",", ":"))
        message = "{0}:::{1}".format(type, data)
    else:
        message = "{0}::".format(type)

    return message

def _parse_message(message):
    type, data = message.split("::", 1)

    try:
        data = json.loads(data[1:])
    except (json.JSONDecodeError) as e:
        data = None
        
    try:
        return int(type), data
    except (ValueError) as e:
        return None, None


class WSSClient():
    __slots__ = ("client", "logger", "loop", "app_id", "recv_handler_task",
                 "room_data", "room_id", "user_id", "ws", "customer_blob",
                 "room_blob", "player")

    def __init__(self, client):
        self.client = client
        self.logger = client.logger
        self.loop = client.loop

        # populated in HTTPClient.connect
        self.app_id = None
        self.recv_handler_task = None
        self.room_data = None
        self.room_id = None
        self.user_id = None
        self.ws = None

        # populated in WSSClient.dispatch_*
        self.customer_blob = None
        self.room_blob = None
        self.player = None

    def clear(self):
        self.app_id = None
        self.recv_handler_task = None
        self.room_data = None
        self.room_id = None
        self.ws = None

        self.customer_blob = None
        self.room_blob = None
        self.player = None

    # connection

    async def _recv_handler(self):
        while True:
            type, data = await self._recv()

            if type == 0:
                # close connection
                await self.close(pass_close=True)
                return # complete the task
            elif type == 1:
                # open connection
                await self.client.dispatch("connect")
            elif type == 2:
                # heartbeat
                await self._send(2)
            elif type == 3:
                # ¯\_(ツ)_/¯
                ...
            elif type == 4:
                # ¯\_(ツ)_/¯
                ...
            elif type == 5:
                # data
                for (data) in data["args"]:
                    await self.dispatch(data)

    async def _recv(self):
        message = await self.ws.recv()

        await self.client.dispatch("raw_socket_recv", message)
        self.logger.debug("> {0}".format(message))

        type, data = _parse_message(message)

        await self.client.dispatch("socket_recv", type, data)

        return type, data

    async def _send(self, type, data=None):
        await self.client.dispatch("socket_send", type, data)

        message = _build_message(type, data)

        await self.client.dispatch("raw_socket_send", message)
        self.logger.debug("< {0}".format(message))

        await self.ws.send(message)

    async def close(self, *, send_close=False, pass_close=False):
        if not self.ws or (not pass_close and self.ws.closed):
            raise Exception("already closed")

        await self.client._http.close()

        try:
            if send_close:
                await self._send(0)
        finally:
            await self.ws.close()

        self.client._http.clear()
        self.clear()

        await self.client.dispatch("close")

    async def connect(self, code, name):
        if self.ws and not self.ws.closed:
            raise Exception("already connected")

        self.room_id = code
        self._generate_uuid()

        self.room_data, ws_id = await self.client._http.connect(code)
        self.app_id = self.room_data["appid"]

        ws_uri = _WS_URI.format(self.room_data["server"], ws_id)
        self.ws = await websockets.connect(ws_uri)

        # check the first recv
        type, _ = await asyncio.wait_for(self._recv(), timeout=5)
        if type != 1:
            raise Exception("i couldn't tell you why this is happening")

        await self.client.dispatch("connect")

        self.recv_handler_task = self.loop.create_task(self._recv_handler())

        await self.join(name, self.room_data["joinAs"])

    # dispatching

    async def dispatch(self, data):
        try:
            ws_event_type = _WS_EVENT_KEY_MAP[data["type"]]
            ws_event_name = data[ws_event_type]

            method = _WS_EVENT_MAP[ws_event_name]
            method = getattr(self, "dispatch_{0}".format(method))

            await method(data)
        except (KeyError) as e:
            self.logger.warning("unhandled data: {0}".format(data))

    async def dispatch_customer_blob_changed(self, data):
        blob = data["blob"]

        if blob != self.customer_blob:
            cls, _ = _BLOB_TYPE_MAP[self.room_data["apptag"]]
            
            try:
                before = self.customer_blob and cls.from_data(self.customer_blob)
                after = cls.from_data(blob)
            except (ValueError) as e:
                # blob constructors can raise ValueError to cancel a
                # *_blob_changed dispatch
                return

            await self.client.dispatch("customer_blob_changed", before, after)
            self.customer_blob = blob

    async def dispatch_room_blob_changed(self, data):
        blob = data["blob"]

        if blob != self.room_blob:
            _, cls = _BLOB_TYPE_MAP[self.room_data["apptag"]]

            try:
                before = self.room_blob and cls.from_data(self.room_blob)
                after = cls.from_data(blob)
            except (ValueError) as e:
                # blob constructors can raise ValueError to cancel a
                # *_blob_changed dispatch
                return

            await self.client.dispatch("room_blob_changed", before, after)
            self.room_blob = blob

    async def dispatch_room_destroy(self, data):
        await self.client.dispatch("room_destroy", data["roomId"])

        self.player = None

    async def dispatch_room_join(self, data):
        if data["success"] is False:
            raise Exception("failed to join")

        cls = _PLAYER_TYPE_MAP[data["joinType"]]
        self.player = cls.from_data(data)

        await self.client.dispatch("room_join", data["roomId"], self.player)

    # game
        
    async def join(self, name, type):
        data = {
            "args": [{
                "action": "JoinRoom",
                "appId": self.app_id,
                "joinType": type,
                "name": name,
                "roomId": self.room_id,
                "type": "Action",
                "userId": self.user_id,
            }],
            "name": "msg",
        }

        await self._send(5, data)

    async def start_countdown(self):
        message = _START_COUNTDOWN_MAP[self.room_data["apptag"]]

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self.app_id,
                "message": message,
                "roomId": self.room_id,
                "type": "Action",
                "userId": self.user_id,
            }],
            "name": "msg",
        }

        await self._send(5, data)

    async def cancel_countdown(self):
        message = _CANCEL_COUNTDOWN_MAP[self.room_data["apptag"]]

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self.app_id,
                "message": message,
                "roomId": self.room_id,
                "type": "Action",
                "userId": self.user_id,
            }],
            "name": "msg",
        }

        await self._send(5, data)

    # helpers

    def _generate_uuid(self):
        # xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx

        if self.user_id is None:
            a = random.randrange(0, 16 ** 8)
            b = random.randrange(0, 16 ** 4)
            c = random.randrange(0, 16 ** 3)
            d = random.randrange(8, 12)
            e = random.randrange(0, 16 ** 3)
            f = random.randrange(0, 16 ** 12)

            parts = (a, b, c, d, e, f)
            self.user_id = "{0:08x}-{1:04x}-4{2:03x}-{3:01x}{4:03x}-{5:012x}".format(*parts)
