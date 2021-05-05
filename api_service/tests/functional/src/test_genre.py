from pathlib import Path

import pytest

from ..testdata.test_parameters.genre_params import (
    default_params
)
from ..utils.get_data_from_file import get_data_from_file

parent_dir = Path(__file__).parents[1]
files_dir = parent_dir.joinpath("testdata", "expected_data", "genres")


@pytest.mark.parametrize(
    "query_params, expected_data_file, status, page_size",
    [
        *default_params,
    ],
)
@pytest.mark.asyncio
async def test_genre_list(
        make_get_request,
        query_params: dict,
        expected_data_file: str,
        status: int,
        page_size: int,
):
    """
    Проверка запроса списка жанров
    """
    response = await make_get_request("/genre", query_params)

    # Проверка статуса ответа
    assert response.status == status

    if expected_data_file is not None:
        # Проверка соответствия ответа содержимому файла
        expected_data = get_data_from_file(files_dir, expected_data_file)
        assert len(response.body) == page_size
        assert response.body == expected_data
