import json
from pathlib import Path
from urllib.parse import urljoin

import pytest as pytest
import requests as requests

from .settings import TestSettings
from .utils import bulk_insert

TEST_DATA_DIR = Path(__file__).parent.joinpath("testdata")

settings = TestSettings()


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
