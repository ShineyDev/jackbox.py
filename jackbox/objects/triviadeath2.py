"""
/jackbox/objects/triviadeath2.py

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

from jackbox.objects import Object


class TriviaMurderParty2Choice(Object):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        kwargs["color"] = data.get("color")
        kwargs["disabled"] = data.get("disabled", False)
        kwargs["index"] = data.get("index")
        kwargs["key"] = data.get("key")
        kwargs["position"] = data.get("position")

        return kwargs