from gather_manager.typeclass.gatherable import Gatherable

from aiohttp import (
    ClientSession,
    ClientResponseError,
    ClientConnectionError,
    ClientPayloadError,
    ClientTimeout,
)

class TooManyRequestsError(ClientResponseError):
    pass

class NotFoundError(ClientResponseError):
    pass

class ForbiddenError(ClientResponseError):
    pass

class ServerError(ClientResponseError):
    pass

class DownloadLink(Gatherable):
    def __init__(self, url_formatter, specifier):
        self.url_formatter = url_formatter
        self.specifier = specifier

    async def gather(self):
        download_url = self.url_formatter(self.specifier)

        try:
            async with ClientSession() as session:
                async with session.get(download_url) as response:
                    # Handle specific HTTP status codes
                    if response.status == 429:
                        retry_after = response.headers.get("Retry-After", "1")
                        raise TooManyRequestsError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"Too many requests. Retry after {retry_after} seconds.",
                        )
                    elif response.status == 404:
                        raise NotFoundError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message="Resource not found (404).",
                        )
                    elif response.status == 403:
                        raise ForbiddenError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message="Access forbidden (403).",
                        )
                    elif 500 <= response.status < 600:
                        raise ServerError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"Server error ({response.status}).",
                        )
                    elif response.status != 200:
                        raise ClientResponseError(
                            request_info=response.request_info,
                            history=response.history,
                            status=response.status,
                            message=f"Unexpected status: {response.status}",
                        )

                    print(response.status)
                    # Return content if status is 200
                    return await response.content.read()

        # Handle broader network-level errors
        except ClientResponseError as e:
            print(f"HTTP Error {e.status}: {e.message}")
            raise e
        except ClientConnectionError as e:
            print(f"Connection Error: {e}")
            raise e
        except ClientPayloadError as e:
            print(f"Payload Error: {e}")
            raise e
        except ClientTimeout as e:
            print(f"Timeout Error: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e

