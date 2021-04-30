import pytest
import aiohttp
from elasticsearch import AsyncElasticsearch

from utils.HTTPResponse import HTTPResponse
from settings import TestSettings

settings = TestSettings()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = settings.api_base_url + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=settings.es_host)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()