import aiohttp

from apexpy.exceptions import ApiKeyNotProvidedError
from apexpy.utils import Constants


class ApexRequest:
    """
    Represents the asynchronous http call made to the apex legends api

    Parameters
    ----------
        name : :class:`str`
            Player's name
        platform : :class:`str`
            Platform numeric code
        api_key : :class:`str`
            Apex key, if not provided directly it'll be looked in os.environ

    Attributes
    ----------

        platform
        name
        api_key
        headers
            :class:`dict`
            Headers sent with the call {'TRN-Api-KEY': key}
        self.req_url
            :class:`str`
            End point


    """
    def __init__(self, name: str, platform: int, api_key: str = None):

        if api_key is None and Constants.API_KEY is None:
            raise ApiKeyNotProvidedError

        self.platform = platform
        self.name = name

        self.api_key = api_key if api_key else Constants.API_KEY
        self.headers = {'TRN-Api-KEY': self.api_key}

        self.req_url = f'{Constants.BASE_URL}{self.platform}/{self.name}'
        self._raw_json = None

    @staticmethod
    async def _error_handler(resp: int) -> None:
        """
        If the api's response is other than 200 (OK) an error will be raised depending on the receive code.
        :param resp: :class:`int`
        :return: :class:`None`
        """
        if resp != Constants.API_OK:
            raise Constants.API_ERROR_MAP.get(resp)

    async def session(self) -> aiohttp.client.ClientResponse:
        """
        Makes the api call.
        :return: :class:`aiohttp.client.ClientResponse`
        """
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.req_url) as resp:
                await self._error_handler(resp.status)
                self._raw_json = await resp.json()
                return resp
