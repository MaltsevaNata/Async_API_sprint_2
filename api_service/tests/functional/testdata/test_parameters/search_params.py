import pytest

# Формат параметров: model, query_params, expected_data, status, page_size

query_params = [
    # совпадения по заголовку фильма и описанию с параметрами страницы
    ("film", {"query": "captain"}, "query_captain.json", 200, 34),
    ("film", {"query": "star", "page_size": 10, "page_number": 1},
     "query_star_page_1_size_10.json", 200, 10),

    # запрос к несуществующим страницам
    pytest.param("film", {"query": "star", "page_size": 10, "page_number": 100},
                 None, 204, None, marks=pytest.mark.skip(reason="Fix response status 200->204 or 404")),

    # отрицательный номер страницы
    pytest.param("film", {"query": "star", "page_number": -1},
                 None, 422, None, marks=pytest.mark.skip(reason="ES throws exception. Fix response status "
                                                                "500->422")),

    # поиск по нескольким словам
    ("film", {"query": "Captain James T. Kirk", "page_size": 100}, "query_Captain_James_size_1000.json",
     200, 46)
]
