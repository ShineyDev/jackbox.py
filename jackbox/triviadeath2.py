"""
/jackbox/triviadeath2.py

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

from jackbox.client import Client


class TriviaMurderParty2Client(Client):
    async def choose(self, index: int):
        """
        |coro|

        Chooses an answer to a ``Question``.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"action": "choose",
                            "choice": index},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)
        
    async def click(self, position: str):
        """
        |coro|

        Clicks a position in a ``Skewers`` minigame.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"action": "click",
                            "position": position},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def draw(self, *points: tuple):
        """
        |coro|

        Draws.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"action": "line",
                            "line": {"color": "#000000",
                                     "points": "|".join("{0},{1}".format(*point) for (point) in points),
                                     "thickness": 1}},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def drop(self, value: int):
        """
        |coro|

        Drops the disc in a ``Pegs`` minigame.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"action": "drop",
                            "value": value},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def reboot(self):
        """
        |coro|

        Restarts the game.
        """

        await self.choose(1)
        
    async def roll(self):
        """
        |coro|

        Rolls a die in the ``Skull Dice`` or ``High Rollers`` minigame.
        """

        await self.choose(0)
        
    async def scratch(self, index: int):
        """
        |coro|

        Scratches a segment in the ``Scratch Off`` minigame.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"action": "scratch",
                            "index": index},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def sequel(self):
        """
        |coro|

        Restarts the game with the same players.
        """

        await self.choose(0)
        
    async def skip(self):
        """
        |coro|

        Skips the intro.
        """

        await self.choose(0)
        
    async def spin(self):
        """
        |coro|

        Spins the wheel in the ``Loser Wheel`` minigame.
        """

        await self.choose(0)

    async def type(self, text: str):
        """
        |coro|

        Types.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"entry": str(text)},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def vote(self, key: str):
        """
        |coro|

        Audience implementation of :meth:`.choose`.
        """

        data = {
            "args": [{
                "action": "SendSessionMessage",
                "appId": self._wss.app_id,
                "message": {"type": "vote",
                            "vote": key},
                "module": "vote",
                "name": "TriviaDeath2 Vote",
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)
