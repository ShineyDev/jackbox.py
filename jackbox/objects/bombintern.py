"""
/jackbox/objects/bombintern.py

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


class BombCorpRule(Object):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        kwargs["body"] = data["body"]
        kwargs["header"] = data["header"]

        return kwargs

class BombCorpTrigger(Object):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()
        
        # all puzzles
        kwargs["index"] = int(data["index"])

        kwargs["fulfilled"] = ((data.get("count") == data.get("target") and
                                data.get("count") is not None) or
                               data.get("hasBeenCut") or
                               data.get("hasBeenFiled") or
                               data.get("hasBeenSmashed") or
                               False)

        # ``.needs_fulfil`` is not identical to ``not .fulfilled``
        kwargs["needs_fulfil"] = (data.get("count") != data.get("target") or
                                  data.get("cut") or
                                  data.get("smash") or
                                  False)
        
        kwargs["priority"] = data["priority"]
        
        # COFFEEBOMB
        kwargs["count"] = data.get("count")
        kwargs["ingredient"] = data.get("ingredient")
        kwargs["target"] = data.get("target")

        # COPIERBOMB
        kwargs["options"] = data.get("options")
        kwargs["name"] = data.get("name")

        # FILINGBOMB
        kwargs["first_name"] = data.get("firstName")
        kwargs["full_name"] = data.get("fullName")
        kwargs["last_name"] = data.get("lastName")
        kwargs["middle_name"] = data.get("middleName")

        # SMASHPUZZLE
        kwargs["object"] = data.get("object")

        # WIREDBOMB
        kwargs["actual_color"] = kwargs["actual_colour"] = data.get("actualColor")
        kwargs["color"] = kwargs["colour"] = data.get("color")
        kwargs["parity"] = data.get("parity")

        return kwargs