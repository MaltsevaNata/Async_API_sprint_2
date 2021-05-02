from pathlib import Path

import pytest

from testdata.test_parameters.search_params import film_search_params
from utils.get_data_from_file import get_data_from_file

parent_dir = Path(__file__).parents[1]
files_dir = parent_dir.joinpath("testdata", "expected_data", "search")


@pytest.mark.parametrize("model, query, expected_data_file, status, page_size",
                         [*film_search_params
                          ])
@pytest.mark.asyncio
async def test_search(make_get_request, model: str, query: dict, expected_data_file: str,
                      status: int, page_size: int):
    """
    Проверка запросов поиска для всех моделей
    """
    response = await make_get_request(f"""/{model}/search/""", query)

    # Проверка статуса ответа
    assert response.status == status

    if expected_data_file is not None:
        # Проверка соответствия ответа содержимому файла
        expected_data = get_data_from_file(files_dir, expected_data_file)
        assert len(response.body) == page_size
        assert response.body == expected_data
