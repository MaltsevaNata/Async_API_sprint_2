import json
from pathlib import Path

import pytest

parent_dir = Path(__file__).parents[1]
expected_data_dir = parent_dir.joinpath("testdata", "expected_data", "films")

default_query = ({}, "film_list_default.json", 200, 50)


@pytest.mark.parametrize("query_params, expected_data_file, status, page_size",
                         [({}, "film_list_default.json", 200, 50),
                          ({"sort": "imdb_rating"}, "film_list_default.json", 200, 50),
                          ({"sort": "-imdb_rating"}, "film_list_desc_sorted.json", 200, 50),
                          ({"sort": "rating"}, None, 422, None),
                          ({"page_number": 0}, "film_list_default.json", 200, 50),
                          ({"page_number": 15}, "film_list_page_number_15.json", 200, 50),
                          ({"page_number": 19}, "film_list_page_number_19.json", 200, 49),
                          ({"page_number": "two"}, None, 422, None),
                          pytest.param({"page_number": 20}, None, 204, None,
                                       marks=pytest.mark.xfail(reason="Fix response status 200->204")),
                          pytest.param({"page_number": -1}, None, 422, None,
                                       marks=pytest.mark.xfail(reason="Fix response status 500->422"))
                          ])
@pytest.mark.asyncio
async def test_film_list_with_params(make_get_request, query_params, expected_data_file, status, page_size):
    """
    Проверка запроса списка фильмов с передачей параметров
    """
    response = await make_get_request('/film', query_params)

    # Проверка статуса ответа
    assert response.status == status

    if expected_data_file:
        # загрузка ожиадемого результата из файла и проверка
        # соответствия ответа содержимому файла
        file = expected_data_dir.joinpath(expected_data_file)
        with open(file, encoding="utf-8") as json_file:
            expected = json.load(json_file)
        assert len(response.body) == page_size
        assert response.body == expected
