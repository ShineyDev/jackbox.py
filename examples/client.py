"""
/examples/client.py
"""

import asyncio

import jackbox


client = jackbox.Client()

@client.listen()
async def on_raw_socket_send(ctx, message):
    if len(message) > 120:
        message = message[:115] + "..."

    print("< {0}".format(message))

@client.listen()
async def on_raw_socket_recv(ctx, message):
    if len(message) > 118:
        message = message[:115] + "..."

    print("> {0}".format(message))

@client.listen()
async def on_connect(ctx):
    print(f"connection opened")

@client.listen()
async def on_room_join(ctx, room, player):
    print(f"joined '{room}' as '{player.name}'")

@client.listen()
async def on_customer_blob_changed(ctx, before, after):
    print("customer blob changed")

@client.listen()
async def on_room_blob_changed(ctx, before, after):
    print("room blob changed")

@client.listen()
async def on_room_destroy(ctx, room):
    print(f"room '{room}' was destroyed :C")

@client.listen()
async def on_close(ctx):
    print("connection closed")


async def run(code):
    await client.connect(code, "listener")
