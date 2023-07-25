from discord.ext import tasks
import sys
sys.path.append("..") 
from config import bot, gen3List, helius_tk #type: ignore
import aiohttp

@tasks.loop(minutes=10)
async def update_gen3():
    await bot.wait_until_ready()
    link = f"https://rpc.helius.xyz/?api-key={helius_tk}"
    gen3list = []
    page = 1
    while True:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAssetsByGroup",
            "params": {
                "groupKey": "collection",
                "groupValue": "8Rt3Ayqth4DAiPnW9MDFi63TiQJHmohfTWLMQFHi4KZH",
                "page": page,
                "limit": 1000,
            }
        }
        async with aiohttp.ClientSession() as session:
            result = await session.post(link, json=payload)
            json = await result.json()
            for item in json['result']['items']:
                needed_data = {"name":item['content']['metadata']['name'], "imageUri":item['content']['files'][0]['uri'], "attributes":item['content']['metadata']['attributes'], "onchainId":item['id']}
                gen3list.append(needed_data)
            if json['result']['total'] < json['result']['limit']:
                break
            page += 1
    gen3List = gen3list
            