class GatherManager:
    def __init__(self, storage):
        """
        Initialize the GatherManager with an AsyncStorage instance.
        """
        self.storage = storage

    async def gather(self, gatherable: Gatherable):
        """
        Execute the gather method of a Gatherable and save the resulting payload to Storage.

        :param gatherable: An instance of a class implementing the Gatherable protocol.
        """
        try:
            payload = await gatherable.gather(storage)
            await self.storage.async_save(payload)
        except Exception as e:
            print(f"Error during gathering: {e}")
            raise