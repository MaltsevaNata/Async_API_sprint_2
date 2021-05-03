import json
from pathlib import Path
from urllib.parse import urljoin
import asyncio
from dataclasses import dataclass
from multidict import CIMultiDictProxy

import pytest
import requests
import aiohttp

from .settings import TestSettings
from .utils import bulk_insert

TEST_DATA_DIR = Path(__file__).parent.joinpath("testdata")

settings = TestSettings()


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int
      
      
@pytest.fixture(scope="session", autouse=True)
def setup_indices():
    """
    Создать необходимые индексы в ES и заполнить их данными.
    """
    indices = "movies persons genres".split()

    for index in indices:
        with TEST_DATA_DIR.joinpath("elastic", f"{index}.json").open() as file:
            data = json.load(file)
        requests.put(urljoin(settings.es_host, index))
        bulk_insert(settings.es_host, index, data)

    yield

    for index in indices:
        requests.delete(urljoin(settings.es_host, index))
     

@pytest.fixture(scope="function")
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


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
