"""
/jackbox/objects/player.py

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

from jackbox.enums import PlayerType
from jackbox.objects import Object


class Player(Object):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        # this data comes from the server and thus should always
        # contain the same keys, no blob craziness here :@
        kwargs["email"] = data["options"]["email"]
        kwargs["id"] = data["userId"]
        kwargs["name"] = data["options"]["name"]
        kwargs["phone"] = data["options"]["phone"]
        kwargs["type"] = PlayerType.try_value(data["joinType"].upper())

        return kwargs

class AudiencePlayer(Player):
    pass
