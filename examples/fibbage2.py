"""
/examples/fibbage2.py
"""

import asyncio

import jackbox


client = jackbox.Client()

@client.listen()
async def on_raw_socket_send(ctx, message):
    print("< {0}\n".format(message))

@client.listen()
async def on_raw_socket_recv(ctx, message):
    print("> {0}\n".format(message))

@client.listen()
async def on_customer_blob_changed(ctx, blob):
    if not blob:
        return
    if not "state" in blob.keys():
        return

    if blob["state"] == "Lobby_PickBloop":
        data = {
            "args": [{
                "action": "SendMessageToRoomOwner",
                "appId": ctx.client._http._app_id,
                "message": {"bloop": blob["bloops"][0]["id"]},
                "roomId": ctx.client._http._room_id,
                "type": "Action",
                "userId": ctx.client._http._user_id,
            }],
            "name": "msg",
        }

        await ctx.client._http._send(5, data)


async def run(code):
    await client.connect(code, "fibbage2")
