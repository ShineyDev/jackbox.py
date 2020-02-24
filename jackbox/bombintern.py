"""
/jackbox/bombintern.py

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


class BombCorpClient(Client):
    async def add(self, ingredient: str):
        """
        |coro|

        Adds an ingredient to a ``CoffeeBomb``.

        Parameters
        ----------
        ingredient: :class:`str`
            The ingredient to add.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"add": True,
                            "ingredient": ingredient},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def brew(self):
        """
        |coro|

        Brews the ``CoffeeBomb``.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"brew": True},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def cut(self, index: int):
        """
        |coro|

        Cuts a wire on a ``WiredBomb``.

        Parameters
        ----------
        index: :class:`int`
            The index of the wire.

            .. note::

                Indexing starts at ``1``.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"index": index},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def file(self, name: str):
        """
        |coro|

        Files a file on a ``FilingBomb``.

        Parameters
        ----------
        name: :class:`str`
            The **full** name of the file.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"file": name},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def menu(self):
        """
        |coro|

        Returns to the menu.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"decision": "Gameover_Menu"},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def next_day(self):
        """
        |coro|

        Starts the next day.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"decision": "Gameover_Continue"},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)
        
    async def press(self, index: int):
        """
        |coro|

        Presses a button on a ``CopierBomb`` or a ``KeypadBomb``.

        Parameters
        ----------
        index: :class:`int`
            The index of the button.

            .. note::

                Indexing starts at ``1``.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"index": index},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)
        
    async def remove(self, ingredient: str):
        """
        |coro|

        Removes an ingredient from a ``CoffeeBomb``.

        Parameters
        ----------
        ingredient: :class:`str`
            The ingredient to remove.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"remove": True,
                            "ingredient": ingredient},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def retry_day(self):
        """
        |coro|

        Retries the current day.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"decision": "Gameover_Retry"},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)

    async def smash(self, name: str):
        """
        |coro|

        Smashes an object on a ``SmashPuzzle``.

        Parameters
        ----------
        name: :class:`str`
            The name of the object.
        """

        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": self._wss.app_id,
                "message": {"object": name},
                "roomId": self._wss.room_id,
                "type": "Action",
                "userId": self._wss.user_id,
            }],
            "name": "msg",
        }

        await self._wss._send(5, data)
