import asyncio
from functions import videoProcessing
from identifier import Identifier

i = Identifier()

asyncio.ensure_future(videoProcessing(i,True))
