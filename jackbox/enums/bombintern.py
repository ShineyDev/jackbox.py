"""
/jackbox/enums/bombintern.py

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

from jackbox.enums import Enum


class BombCorpState(Enum):
    none = None

    # general
    lobby              = "LOBBY"             # R  state=Lobby
    lobby_can_start    = "CANSTART"          #  C state=CanStart
    lobby_countdown    = "COUNTDOWN"         #  C state=Countdown
    lobby_waiting      = "WAITINGFORMORE"    #  C state=WaitingForMore
    logo               = "LOGO"              # R  state=Logo

    # game
    day_end            = "DAYEND"            # R  state=DayEnd
    day_end_decision   = "DAYENDDECISION"    #  C state=DayEndDecision
    game_over          = "GAMEOVER"          # R  state=GameOver
    game_over_decision = "GAMEOVERDECISION"  #  C state=GameOverDecision
    message            = "MESSAGE"           # RC state=Message

    # puzzles
    coffee_bomb        = "COFFEEBOMB"        #  C state=CoffeeBomb
    copier_bomb        = "COPIERBOMB"        #  C state=CopierBomb
    filing_bomb        = "FILINGBOMB"        #  C state=FilingBomb
    keypad_bomb        = "KEYPADBOMB"        #  C state=KeypadBomb
    puzzle             = "PUZZLE"            # R  state=Puzzle
    smash_puzzle       = "SMASHPUZZLE"       #  C state=SmashPuzzle
    wired_bomb         = "WIREDBOMB"         #  C state=WiredBomb
