"""
/jackbox/objects/blobs/bombintern.py

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

from jackbox.enums import BombCorpState as BCState
from jackbox.objects import BombCorpRule as BCRule, BombCorpTrigger as BCTrigger
from jackbox.objects.blobs import CustomerBlob, RoomBlob


class BombCorpCustomerBlob(CustomerBlob):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        kwargs["analytics"] = data.get("analytics")
            
        kwargs["player_color"] = kwargs["player_colour"] = data.get("playerColor")
        kwargs["player_name"] = data.get("playerName")

        rules = data.get("rules")
        if rules:
            rules = [BCRule.from_data(rule) for (rule) in rules]

        kwargs["rules"] = rules

        state = (data.get("state") or "").upper() or None
        kwargs["state"] = BCState.try_value(state)

        triggers = data.get("triggers")
        if triggers:
            triggers = [BCTrigger.from_data(trigger) for (trigger) in triggers]

        kwargs["triggers"] = triggers

        kwargs["type"] = data.get("type")

        return kwargs

class BombCorpRoomBlob(RoomBlob):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        state = (data.get("state") or "").upper() or None
        kwargs["state"] = BCState.try_value(state)

        return kwargs
