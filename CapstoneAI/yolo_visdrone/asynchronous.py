import asyncio
from main import Adjusted

async def Catch(bbox):

    info = await Adjusted.detect_annotate()