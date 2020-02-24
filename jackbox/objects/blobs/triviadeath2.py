"""
/jackbox/objects/blobs/triviadeath2.py

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

from jackbox.enums import TriviaMurderParty2Doll as TMP2Doll, TriviaMurderParty2State as TMP2State
from jackbox.objects import TriviaMurderParty2Choice as TMP2Choice
from jackbox.objects.blobs import CustomerBlob, RoomBlob


_IGNORED_STATES = ["Draw", "EnterSingleText", "Gameplay", "Grid",
                   "MakeSingleChoice", None]


class TriviaMurderParty2CustomerBlob(CustomerBlob):
    @staticmethod
    def _check(data):
        if data["choices"] is not None and len(data["choices"]) == 0:
            # happens in ``Math`` and ``Rules`` minigames when choosing
            # an answer before being unfrozen
            return False

        return True

    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        doll = (data.get("dollInfo") or {"id": ""})["id"].upper() or None
        kwargs["doll"] = TMP2Doll.try_value(doll)

        # i'd like to give my deepest apologies to anyone reading this.
        # i am so sorry. tmp2 is a mess.
        state = ((data.get("state") if data.get("state") not in _IGNORED_STATES else None) or
                 (data["audience"]["choiceId"] if data.get("audience") is not None else None) or
                 data.get("choiceType") or
                 data.get("roundType") or
                 (data["entryId"].rstrip("0123456789") if data.get("entryId") is not None else None) or
                 data.get("state") or
                 "").replace(" ", "").upper() or None

        kwargs["state"] = TMP2State.try_value(state)

        choices = data.get("choices")
        if choices:
            for (i, _) in enumerate(choices.copy()):
                choices[i]["index"] = i

        grid = data.get("grid")
        if grid:
            # OH THE WORKAROUNDS
            if grid[0][0]["type"] == "Hide":
                kwargs["state"] = TMP2State.skewers_hide
            else:
                kwargs["state"] = TMP2State.skewers_stab

            choices = list()
            for (x, row) in enumerate(grid):
                for (y, choice) in enumerate(row):
                    if not choice["disabled"]:
                        choice["position"] = "{0}-{1}".format(x, y)
                        choices.append(choice)

        kwargs["choices"] = [TMP2Choice.from_data(choice) for (choice) in choices] if choices is not None else None

        kwargs["prompt"] = data.get("prompt", dict()).get("text") or data.get("prompt", dict()).get("html")
        kwargs["size"] = (data["size"]["width"], data["size"]["height"]) if data.get("size") else None

        if not cls._check(kwargs):
            raise ValueError

        return kwargs

class TriviaMurderParty2RoomBlob(RoomBlob):
    @classmethod
    def _transform_data(cls, data):
        kwargs = dict()

        doll = (data.get("dollInfo") or {"id": ""})["id"].upper() or None
        kwargs["doll"] = TMP2Doll.try_value(doll)

        state = ((data["lobbyState"] if data.get("lobbyState") is not None else None) or
                 (data["state"] if data.get("state") not in _IGNORED_STATES else None) or
                 (data["audience"].get("choiceId") if data.get("audience") is not None else None) or
                 (data["audience"].get("state") if data.get("audience") is not None else None) or
                 data.get("state") or
                 "").upper() or None

        kwargs["state"] = TMP2State.try_value(state)

        choices = (data.get("audience") or data).get("choices")
        if choices:
            for (i, choice) in enumerate(choices.copy()):
                choices[i]["index"] = i

        kwargs["choices"] = [TMP2Choice.from_data(choice) for (choice) in choices] if choices is not None else None

        prompt = (data.get("prompt", dict()).get("text") or
                  data.get("prompt", dict()).get("html") or
                  (data.get("audience") or dict()).get("prompt", dict()).get("text") or
                  (data.get("audience") or dict()).get("prompt", dict()).get("html"))

        if prompt:
            if kwargs["state"] == "AUDIENCECHOICE":
                # thanks jackbox
                if "Guess" in prompt:
                    kwargs["state"] = TMP2State.player_death
                elif data.get("roundType") == "FinalRound":
                    kwargs["state"] = TMP2State.final_round
                else:
                    kwargs["state"] = TMP2State.question

        kwargs["prompt"] = prompt

        return kwargs
