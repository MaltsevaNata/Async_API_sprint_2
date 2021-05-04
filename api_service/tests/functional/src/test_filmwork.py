from pathlib import Path

import pytest

from ..testdata.test_parameters.film_params import (
    combined_params,
    default_params,
    film_id_params,
    genre_params,
    page_num_params,
    page_size_params,
    sort_params,
)
from ..utils.get_data_from_file import get_data_from_file

parent_dir = Path(__file__).parents[1]
files_dir = parent_dir.joinpath("testdata", "expected_data", "films")


@pytest.mark.parametrize(
    "query_params, expected_data_file, status, page_size",
    [
        *default_params,
        *sort_params,
        *page_num_params,
        *page_size_params,
        *genre_params,
        *combined_params,
    ],
)
@pytest.mark.usefixtures("clear_cache")
@pytest.mark.asyncio
async def test_film_list(
    make_get_request,
    query_params: dict,
    expected_data_file: str,
    status: int,
    page_size: int,
):
    """
    Проверка запроса списка фильмов с передачей параметров
    """
    response = await make_get_request("/film", query_params)

    # Проверка статуса ответа
    assert response.status == status

    if expected_data_file is not None:
        # Проверка соответствия ответа содержимому файла
        expected_data = get_data_from_file(files_dir, expected_data_file)
        assert len(response.body) == page_size
        assert response.body == expected_data


@pytest.mark.parametrize("film_id, expected_data_file, status", [*film_id_params])
@pytest.mark.usefixtures("clear_cache")
@pytest.mark.asyncio
async def test_film_by_id(
    make_get_request, film_id: str, expected_data_file: str, status: int
):
    """
    Проверка поиска фильма по id
    """
    response = await make_get_request(f"""/film/{film_id}""", {})

    # Проверка статуса ответа
    assert response.status == status

    if expected_data_file is not None:
        expected_data = get_data_from_file(files_dir, expected_data_file)
        # Проверка соответствия ответа содержимому файла
        assert response.body == expected_data
