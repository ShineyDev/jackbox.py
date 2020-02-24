"""
/examples/bombintern_four.py
"""

import asyncio

import jackbox


clients = [
    jackbox.BombCorpClient(client_attrs={"id": 1}),
    jackbox.BombCorpClient(client_attrs={"id": 2}),
    jackbox.BombCorpClient(client_attrs={"id": 3}),
    jackbox.BombCorpClient(client_attrs={"id": 4}),
]

for (client) in clients:
    @client.listen()
    async def on_raw_socket_send(ctx, message):
        if len(message) > 185:
            message = message[:182] + "..."

        print("< {0} {1}".format(ctx.client.id, message))

    @client.listen()
    async def on_raw_socket_recv(ctx, message):
        if len(message) > 185:
            message = message[:182] + "..."

        print("> {0} {1}".format(ctx.client.id, message))


async def run(n, code):
    for (client) in clients[:n]:
        await client.connect(code, str(client.id))

    await asyncio.sleep(3)
    await clients[0].start_countdown()

    return clients
