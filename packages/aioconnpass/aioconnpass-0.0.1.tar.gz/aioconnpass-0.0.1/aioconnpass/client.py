import aiohttp
import asyncio
import json


class AioConnpassError(Exception):
    def __init__(self, http_status, msg):
        self.http_status = http_status
        self.msg = msg

    def __str__(self):
        return 'http status: {0} - {1}'.format(self.http_status, self.msg)


class Connpass:
    BASE = 'https://connpass.com/api/v1/event/'

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def request(self, params):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE, params=params) as response:
                _json = await response.text()
                status = response.status

        if status != 200:
            raise AioConnpassError(status, "Request failed")

        return json.loads(_json)

    async def search(self, **kwargs):
        """|coro|
        Request to connpass API
        Please see https://connpass.com/about/api/
        Parameters
            event_id: str or list
            keyword: str or list
            keyword_or: str or list
            ym: int For example: 201804 (yyyymm)
            ymd: int For example: 20180401 (yyyymmdd)
            nickname: str
            owner_nickname: str
            series_id: int
            start: int
            order: int
            count: int
        :return: dict
        """
        kwargs['format'] = 'json'
        params = {}
        for key, value in kwargs.items():
            if type(value) == list:
                params[key] = ",".join(value)
            elif type(value) == str:
                params[key] = value
            else:
                raise TypeError("must list or str")
        return await asyncio.wait_for(self.request(params), 30)


if __name__ == "__main__":
    connpass = Connpass()


    async def test():
        t = await connpass.search(keyword="長野")
        print(t)

    asyncio.get_event_loop().run_until_complete(test())
