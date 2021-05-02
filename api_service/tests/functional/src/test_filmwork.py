from typing import Union

import pytest

from testdata.test_parameters.film_list_params import default_params, sort_params, page_num_params, page_size_params
from testdata.test_parameters.film_list_params import film_id_params, genre_params, combined_params


@pytest.mark.parametrize("query_params, expected_data, status, page_size",
                         [*default_params,
                          *sort_params,
                          *page_num_params,
                          *page_size_params,
                          *genre_params,
                          *combined_params
                          ])
@pytest.mark.asyncio
async def test_film_list(make_get_request, query_params: dict, expected_data: list,
                         status: int, page_size: int):
    """
    Проверка запроса списка фильмов с передачей параметров
    """
    response = await make_get_request('/film', query_params)

    # Проверка статуса ответа
    assert response.status == status

    if expected_data is not None:
        # Проверка соответствия ответа содержимому файла
        assert len(response.body) == page_size
        assert response.body == expected_data


@pytest.mark.parametrize("film_id, expected_data, status",
                         [*film_id_params])
@pytest.mark.asyncio
async def test_film_by_id(make_get_request, film_id: str, expected_data: dict, status: int):
    """
    Проверка поиска фильма по id
    """
    response = await make_get_request(f"""/film/{film_id}""", {})

    # Проверка статуса ответа
    assert response.status == status

    if expected_data is not None:
        # Проверка соответствия ответа содержимому файла
        assert response.body == expected_data
