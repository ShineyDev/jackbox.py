"""
/jackbox/client.py

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
import logging

from jackbox import _http, _wss
from jackbox.helpers import context


class Client():
    """
    The base client for connection to a |jackbox_party_pack| game.

    Parameters
    ----------
    loop: :class:`asyncio.Loop`
        The loop to run the client in.
    client_attrs: :class:`dict`
        A map of `attr: value` to add to the :class:`jackbox.Client` class.
    context_attrs: :class:`dict`
        A map of `attr: value` to add to all :class:`jackbox.helpers.Context` classes.

    Attributes
    ----------
    logger: :class:`logging.Logger`
        The client's internal logger.
    loop: :class:`asyncio.Loop`
        The loop the client is running in.
    """

    def __init__(self, *, loop=None, **kwargs):
        self.logger = logging.getLogger("jackbox.py")
        self.loop = loop or asyncio.get_event_loop()

        self._http = _http.HTTPClient(self)
        self._wss = _wss.WSSClient(self)

        self._listeners = dict()

        self._client_attrs = kwargs.get("client_attrs", dict())
        self._context_attrs = kwargs.get("context_attrs", dict())

        for (key, value) in self._client_attrs.items():
            setattr(self, key, value)

    async def dispatch(self, event, *args):
        event = "on_{0}".format(event)

        to_remove = list()

        listeners = self._listeners.get(event, list())
        for (i, listener) in enumerate(listeners):
            if isinstance(listener, asyncio.Future):
                # :attr:`.wait_for`

                if len(args) == 0:
                    listener.set_result(None)
                elif len(args) == 1:
                    listener.set_result(args[0])
                else:
                    listener.set_result(args)

                to_remove.append(i)
            else:
                ctx = context.Context(self, context_attrs=self._context_attrs)
                self.loop.create_task(listener(ctx, *args))

        for (i) in reversed(to_remove):
            del self._listeners[event][i]

    # connection

    async def close(self) -> None:
        """
        |coro|

        Closes the websocket connection to the |jackbox_games| server.
        """

        await self._wss.close(send_close=True)

    async def connect(self, code: str, name: str) -> None:
        """
        |coro|

        Opens a websocket connection to the |jackbox_games| server and
        joins a |jackbox_party_pack| game room.

        Parameters
        ----------
        code: :class:`str`
            The room code.
        name: :class:`str`
            The name of your player.
        """

        await self._wss.connect(code.upper(), name)

    # game

    async def start_countdown(self) -> None:
        """
        |coro|

        Starts the game countdown.
        """

        await self._wss.start_countdown()

    async def cancel_countdown(self) -> None:
        """
        |coro|

        Cancels the game countdown.
        """

        await self._wss.cancel_countdown()

    # helpers
    
    def add_listener(self, func, *, name: str=None):
        """

        """

        if not asyncio.iscoroutinefunction(func):
            raise TypeError("listener callbacks must be coroutines")

        name = name or func.__name__

        if name in self._listeners.keys():
            self._listeners[name].append(func)
        else:
            self._listeners[name] = [func]

    def remove_listener(self, func, *, name: str=None) -> None:
        """

        """

        name = name or func.__name__

        try:
            self._listeners[name].remove(func)
        except (KeyError, ValueError) as e:
            pass

    def listen(self, *, name: str=None):
        """

        """

        def deco(func):
            self.add_listener(func, name=name)
            return func

        return deco

    async def wait_for(self, event, *, timeout: int=None):
        """

        """

        name = "on_{0}".format(event)

        future = self.loop.create_future()

        if name in self._listeners.keys():
            self._listeners[name].append(future)
        else:
            self._listeners[name] = [future]

        result = await asyncio.wait_for(future, timeout)

        self.remove_listener(future, name=name)

        return result
