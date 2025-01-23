from aiohttp import ClientSession
from gather_manager.typeclass.gatherable import Gatherable

class DownloadLink(Gatherable):
    def __init__(self, url_formatter, specifier):
        self.url_formatter = url_formatter
        self.specifier = specifier

    async def gather(self):
        async with ClientSession() as session:
            download_url = self.url_formatter(self.specifier)

            async with session.get(download_url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed Download with status: {respose.status}")

                return await response.content.read()

