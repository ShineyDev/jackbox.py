"""
/examples/bombintern.py
"""

import asyncio
import random

from jackbox import BombCorpClient as BCClient
from jackbox.enums import BombCorpState as BCState


clients = list()


async def _sleep(start, end):
    duration = random.randint(start * 1000, end * 1000) / 1000
    await asyncio.sleep(duration)

def _register_events(client):
    @client.listen()
    async def on_raw_socket_send(ctx, message):
        print("< {0}".format(message))

    @client.listen()
    async def on_raw_socket_recv(ctx, message):
        print("> {0}".format(message))

    @client.listen()
    async def on_customer_blob_changed(ctx, before, after):
        print("CUST", after.state)

        if after.state == BCState.lobby_can_start:
            await asyncio.sleep(3)
            await ctx.client.start_countdown()
        elif after.state == BCState.day_end_decision:
            await asyncio.sleep(3)
            await ctx.client.next_day()
        elif after.state == BCState.game_over_decision:
            await asyncio.sleep(3)
            await ctx.client.retry_day()

        if after.state == BCState.coffee_bomb:
            triggers = [trigger for (trigger) in after.triggers if not trigger.fulfilled]
            
            if triggers:
                trigger = triggers[0]

                await _sleep(0, 1)
                await ctx.client.add(trigger.ingredient)
            else:
                await ctx.client.brew()
        elif after.state == BCState.copier_bomb:
            print(*[rule.body for (rule) in after.rules], sep="\n")
            print(*["{0} {1}".format(trigger.index, trigger.name) for (trigger) in after.triggers], sep="\n")
        elif after.state == BCState.filing_bomb:
            triggers = [trigger for (trigger) in after.triggers if not trigger.fulfilled]
            triggers = sorted(triggers, key=lambda t: t.priority)

            if triggers:
                trigger = triggers[0]

                await _sleep(0, 1)
                await ctx.client.file(trigger.full_name)
        elif after.state == BCState.keypad_bomb:
            print(*[rule.body for (rule) in after.rules], sep="\n")
        elif after.state == BCState.smash_puzzle:
            triggers = [trigger for (trigger) in after.triggers if trigger.needs_fulfil and not trigger.fulfilled]
            triggers = sorted(triggers, key=lambda t: t.priority)

            if triggers:
                trigger = triggers[0]

                await _sleep(0, 1)
                await ctx.client.smash(trigger.object)
        elif after.state == BCState.wired_bomb:
            triggers = [trigger for (trigger) in after.triggers if trigger.needs_fulfil and not trigger.fulfilled]
            triggers = sorted(triggers, key=lambda t: t.priority)

            if triggers:
                trigger = triggers[0]

                await _sleep(0, 1)
                await ctx.client.cut(trigger.index)

    @client.listen()
    async def on_room_blob_changed(ctx, before, after):
        print("ROOM", after.state)


async def run(n, code):
    global clients
    clients = list()

    for (i) in range(0, n):
        client = BCClient()
        
        _register_events(client)
        clients.append(client)

        await client.connect(code, str(i + 1))

    await asyncio.sleep(3)
    await clients[0].start_countdown()
