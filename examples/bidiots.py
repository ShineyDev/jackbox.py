"""
/examples/bidiots.py
"""

import asyncio

import jackbox


client = jackbox.BidiotsClient()


async def run(code):
    await client.connect(code, "bidiots")
