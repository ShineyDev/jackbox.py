"""
/examples/triviadeath2.py
"""

import asyncio
import operator
import random

from jackbox import TriviaMurderParty2Client as TMP2Client
from jackbox.enums import PlayerType, TriviaMurderParty2State as TMP2State


clients = list()


async def _sleep(start, end):
    duration = random.randint(start * 1000, end * 1000) / 1000
    await asyncio.sleep(duration)

def _register_events(client):
    @client.listen()
    async def on_customer_blob_changed(ctx, before, after):
        print("CUST", after.state)

        if after.state == TMP2State.tutorial:
            await asyncio.sleep(1)
            await ctx.client.skip()
        elif after.state == TMP2State.post_game_choice:
            await asyncio.sleep(10)
            await ctx.client.sequel()

        if after.state == TMP2State.player_death:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.choose(choice.index)

        if after.state == TMP2State.question:
            choices = [c for (c) in after.choices if not c.disabled]
            choice = random.choice(choices)

            await _sleep(0, 20)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.final_round:
            choices = after.choices[:-1]
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.choose(choice.index)

        if after.state == TMP2State.chalices_drink:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.chalices_poison:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.donations_amount:
            amount = random.randint(0, 500)

            await _sleep(0, 5)
            await ctx.client.type(amount)
        elif after.state == TMP2State.donations_user:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.dumb_waiters:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 10)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.escape_room:
            print("wait how the fuck did you get", after.state)
        elif after.state == TMP2State.gifts_choose:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.gifts_cut_finger:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.gifts_give:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.greed_amount:
            amount = random.randint(0, 1000)

            await _sleep(0, 5)
            await ctx.client.type(amount)
        elif after.state == TMP2State.high_rollers_give:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.high_rollers_roll:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.lock_and_key:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.loser_wheel:
            await _sleep(0, 5)
            await ctx.client.spin()
        elif after.state == TMP2State.math:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.mirror_draw:
            ...
        elif after.state == TMP2State.mirror_guess:
            words = ["butts", "gloop"]

            word = random.choice(words)

            await _sleep(0, 5)
            await ctx.client.type(word)
        elif after.state == TMP2State.password_create:
            words = ["yell", "whew", "read", "duck", "take",
                     "hell", "jump", "hock", "seep", "blue"]

            word = random.choice(words)

            await _sleep(0, 5)
            await ctx.client.type(word)
        elif after.state == TMP2State.password_guess:
            words = ["yell", "whew", "read", "duck", "take",
                     "hell", "jump", "hock", "seep", "blue"]

            word = random.choice(words)

            await _sleep(0, 5)
            await ctx.client.type(word)
        elif after.state == TMP2State.pegs_bucket:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.pegs_drop:
            index = random.randint(0, 100)

            await _sleep(0, 10)
            await ctx.client.drop(index)
        elif after.state == TMP2State.quiplash:
            print("i didn't implement", after.state, "yet")
        elif after.state == TMP2State.rules:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.choose(choice.index)
        elif after.state == TMP2State.scratch_off:
            choices = [c for (c) in after.choices if c.color == "Gray"]
            choice = random.choice(choices)

            if len(choices) > 6:
                await _sleep(0, 5)
                await ctx.client.scratch(choice.index)
            elif len(choices) > 2:
                to_go = len(choices) - 2

                if random.randrange(0, 9) in range(0, 9)[:to_go]:
                    await _sleep(0, 5)
                    await ctx.client.scratch(choice.index)
        elif after.state == TMP2State.skewers_hide:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.click(choice.position)
        elif after.state == TMP2State.skewers_stab:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.click(choice.position)
        elif after.state == TMP2State.skull_dice:
            try:
                current_n = int(after.prompt.rsplit(" ", 1)[1])
            except (ValueError) as e:
                current_n = 0

            to_go = 21 - current_n
            
            if random.randrange(0, 6 * 2) in range(0, 6)[:to_go]:
                await _sleep(0, 5)
                await ctx.client.roll()
        elif after.state == TMP2State.tattoos_draw:
            ...
        elif after.state == TMP2State.tattoos_vote:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 5)
            await ctx.client.choose(choice.index)
        
    @client.listen()
    async def on_room_blob_changed(ctx, before, after):
        print("ROOM", after.state)

        if ctx.client._wss.player.type != PlayerType.audience:
            return

        if after.state == TMP2State.player_death:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.vote(choice.key)

        if after.state == TMP2State.question:
            choices = after.choices
            choice = random.choice(choices)

            await _sleep(0, 10)
            await ctx.client.vote(choice.key)
        elif after.state == TMP2State.final_round:
            choices = after.choices[:-1]
            choice = random.choice(choices)

            await _sleep(0, 3)
            await ctx.client.vote(choice.key)


async def run(n, code):
    global clients
    clients = list()

    for (i) in range(0, min([n, 8])):
        client = TMP2Client()
        
        _register_events(client)
        clients.append(client)

        await client.connect(code, str(i + 1))

        _, player = await client.wait_for("room_join")
        if player.type == PlayerType.audience:
            break

    for (i) in range(i + 1, n):
        client = TMP2Client()
        client.loop.create_task(client.connect(code, str(i + 1)))

        _register_events(client)
        clients.append(client)

    await asyncio.sleep(3)
    await clients[0].start_countdown()
