import pytest

from functional.conftest import make_get_request


@pytest.mark.asyncio
async def test_film_list(es_client):
    # Заполнение данных для теста
    #await es_client.bulk(...)
    print("I'm here")
    # Выполнение запроса
    response = await make_get_request('/film')

    # Проверка результата
    assert response.status == 200
    #assert len(response.body) == 1

    #assert response.body == expected
