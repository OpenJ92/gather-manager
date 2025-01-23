from typing import Protocol

class Gatherable(Protocol):
    async def gather(self) -> dict:
        """
        Perform the scraping operation and return the scraped data as a payload.
        """
        pass
