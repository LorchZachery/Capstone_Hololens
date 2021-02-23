import asyncio
from main import Adjusted

async def Catch(bbox):
	print("in async catch")
    info = await Adjusted.UpdateBBox()
	print("caught info: " + info)
	