import pytest

from testdata.test_parameters.film_list_params import default_params, sort_params, page_num_params, genre_params


@pytest.mark.parametrize("query_params, expected_data, status, page_size",
                         [*default_params,
                          *sort_params,
                          *page_num_params,
                          *genre_params
                          ])
@pytest.mark.asyncio
async def test_film_list(make_get_request, query_params, expected_data, status, page_size):
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
