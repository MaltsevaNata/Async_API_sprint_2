import json
from pathlib import Path

import pytest

parent_dir = str(Path(__file__).parents[1])
expected_data_dir = parent_dir + "\\testdata\\expected_data\\films\\"


@pytest.mark.asyncio
async def test_film_list_default(make_get_request):
    """
    Проверка запроса списка фильмов без параметров,
    по дефолту сортировка должна быть по возрастанию рейтинга,
    50 записей на странице
    """
    response = await make_get_request('/film', {})

    # загрузка ожиадемого результата из файла
    with open(expected_data_dir + 'film_list_default.json') as json_file:
        expected = json.load(json_file)

    # Проверка результата
    assert response.status == 200
    assert len(response.body) == len(expected)
    # print(expected[5]) вот в этих строчках ошибка
    # print(response.body[5])
    assert response.body == expected
