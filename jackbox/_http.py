"""
/jackbox/_http.py

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

import json
import time

import aiohttp


_SV_URI = "http://blobcast.jackboxgames.com/room/{0}"
_ID_URI = "https://{0}:38203/socket.io/1?t={1}"


class HTTPClient():
    __slots__ = ("client", "logger", "loop", "session")

    def __init__(self, client):
        self.client = client
        self.logger = client.logger
        self.loop = client.loop
        
        # populated in HTTPClient.connect
        self.session = None

    def clear(self):
        self.session = None

    # connection

    async def close(self):
        await self.session.close()

    async def connect(self, code):
        self.session = aiohttp.ClientSession()

        # room_data

        sv_uri = _SV_URI.format(code)

        async with self.session.get(sv_uri) as response:
            text = await response.text()

            try:
                room_data = json.loads(text)
            except (json.JSONDecodeError) as e:
                raise Exception("invalid room code")

        if room_data["joinAs"] == "full":
            raise Exception("room full")

        # ws_id

        id_uri = _ID_URI.format(room_data["server"], int(time.time() * 1000))
        
        async with self.session.get(id_uri) as response:
            text = await response.text()
            ws_id, *_, type = text.split(":")
            
            if not all([n == "60" for (n) in _]):
                await self.close()
                raise Exception("what do these numbers mean")
            elif "websocket" not in type:
                await self.close()
                raise Exception("somehow not websocket")

        return (room_data, ws_id)
