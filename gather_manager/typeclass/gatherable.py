class Gatherable(Protocol):
    async def gather(self, storage) -> dict:
        """
        Perform the scraping operation and return the scraped data as a payload.
        """
        pass
