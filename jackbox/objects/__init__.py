"""
/jackbox/objects/__init__.py

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

class Object():
    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    @staticmethod
    def _check(data):
        raise NotImplementedError

    @classmethod
    def _transform_data(cls, data):
        raise NotImplementedError

    @classmethod
    def from_data(cls, data):
        return cls(data=data, **cls._transform_data(data))


from jackbox.objects.player import AudiencePlayer, Player

from jackbox.objects.bombintern import BombCorpRule, BombCorpTrigger


_PLAYER_TYPE_MAP = {
    "audience": AudiencePlayer,
    "player": Player,
}
