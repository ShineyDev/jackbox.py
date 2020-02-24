"""
/jackbox/enums/triviadeath2.py

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


class TriviaMurderParty2Doll(Enum):
    audience    = "AUDIENCE"

    alpha       = "ORANGE"
    believer    = "BLUE"
    jester      = "PURPLE"
    lovers      = "PINK"
    nerd        = "GRAY"
    red_herring = "RED"
    screamer    = "YELLOW"
    sheriff     = "GREEN"

class TriviaMurderParty2State(Enum):
    none = None

    # general
    gameplay          = "GAMEPLAY"                 # RC state=Gameplay
    lobby             = "LOBBY"                    # R  state=Lobby
    lobby_can_start   = "CANSTART"                 #  C lobbyState=CanStart
    lobby_countdown   = "COUNTDOWN"                #  C lobbyState=Countdown
    logo              = "LOGO"                     # R  state=Logo

    # game
    post_game_choice  = "POSTGAMECHOICE"           #  C choiceType=PostGameChoice
    tutorial          = "SKIPTUTORIAL"             #  C choiceType=SkipTutorial

    # audience
    player_death      = "PLAYERDEATH"              # RC choiceType=PlayerDeath

    # game
    final_round       = "FINALROUND"               # RC roundType=FinalRound
    question          = "QUESTION"                 # RC choiceType=Question

    # minigames
    chalices_drink    = "DRINKCHALICE"             #  C choiceType=Drink Chalice
    chalices_poison   = "POISONCHALICE"            #  C choiceType=PoisonChalice
    dictation         = "DICTATION"                #  C entryId=Dictation
    donations_amount  = "DONATIONAMOUNT"           #  C entryId=DonationAmount
    donations_user    = "CHOOSEDONATIONRECIPIENT"  #  C choiceType=ChooseDonationRecipient
    dumb_waiters      = "SCALE"                    #  C choiceType=Scale
    escape_room       = ""                         # 
    gifts_choose      = "CHOOSEGIFT"               #  C choiceType=ChooseGift
    gifts_cut_finger  = "CUTFINGER"                #  C choiceType=CutFinger
    gifts_give        = "WILLITEM"                 #  C choiceType=WillItem
    greed_amount      = "GREEDYNUMBER"             #  C entryId=GreedyNumber
    high_rollers_give = "HIGHROLLGIVEDIE"          #  C choiceType=HighRollGiveDie
    high_rollers_roll = "HIGHROLLDICE"             #  C choiceType=HighRollDice
    lock_and_key      = "TAKEKEY"                  #  C choiceId=TakeKey
    loser_wheel       = "SPINWHEEL"                #  C choiceType=SpinWheel
    math              = "MATH"                     #  C choiceType=Math
    mind_meld         = "MINDMELD"                 #  C entryId=MindMeldN
    mirror_draw       = "MIRROR"                   #  C roundType=Mirror
    mirror_guess      = "MIRRORGUESS"              #  C entryId=MirrorGuess
    password_create   = "CREATEPASSWORD"           #  C entryId=CreatePassword
    password_guess    = "PASSWORD"                 #  C roundType=Password
    pegs_bucket       = "CHOOSEBUCKET"             #  C choiceType=ChooseBucket
    pegs_drop         = "DROP"                     #  C state=Drop
    phones            = "DIAL"                     #  C state=Dial
    quiplash          = "QUIPLASH"                 #  C entryId=Quiplash
    rules             = "RULE"                     #  C choiceType=Rule
    scratch_off       = "SCRATCH"                  #  C state=Scratch
    skewers_hide      = "GRIDHIDE"                 #  C state=Grid
    skewers_stab      = "GRIDSTAB"                 #  C state=Grid
    skull_dice        = "SKULLDICE"                #  C choiceType=SkullDice
    tattoos_draw      = "TATTOOS"                  #  C roundType=Tattoos
    tattoos_vote      = "TATTOOVOTE"               #  C choiceType=TattooVote
