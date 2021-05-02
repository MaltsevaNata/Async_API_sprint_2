import json
from typing import Union

import pytest

from pathlib import Path

parent_dir = Path(__file__).parents[1]
files_dir = parent_dir.joinpath("expected_data", "films")


def get_data_from_file(expected_data_file: str) -> Union[list, dict]:
    file = files_dir.joinpath(expected_data_file)
    with open(file, encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


# Format of parameters: (query_params, expected_data_list, response_status, page_size)
default_params = [({}, get_data_from_file("film_list_default.json"), 200, 50)]

sort_params = [({"sort": "imdb_rating"}, get_data_from_file("film_list_default.json"), 200, 50),
               ({"sort": "-imdb_rating"}, get_data_from_file("film_list_desc_sorted.json"), 200, 50),
               ({"sort": "rating"}, None, 422, None)]

page_num_params = [({"page_number": 0}, get_data_from_file("film_list_default.json"), 200, 50),
                   ({"page_number": 15}, get_data_from_file("film_list_page_number_15.json"), 200, 50),
                   ({"page_number": 19}, get_data_from_file("film_list_page_number_19.json"), 200, 49),
                   ({"page_number": "two"}, None, 422, None),
                   pytest.param({"page_number": 20}, None, 204, None,
                                marks=pytest.mark.skip(reason="Fix response status 200->204")),
                   pytest.param({"page_number": -1}, None, 422, None,
                                marks=pytest.mark.skip(reason="ES throws exception. Fix response status 500->422"))]

genre_params = [({"genre": "Documentary"}, get_data_from_file("film_list_genre_documentary.json"), 200, 50),
                ({"genre": "Reality-TV"}, get_data_from_file("film_list_genre_realitytv.json"), 200, 38),
                ({"genre": "Cartoon"}, [], 200, 0)]

# Format of parameters: (film_id, expected_data_list, response_status)
film_id_params = [('f92c6b11-3f73-4c3f-a9e3-85b1bb91284b',
                   get_data_from_file("film_id_f92c6b11-3f73-4c3f-a9e3-85b1bb91284b.json"), 200),
                  ('5a5f31ab-d212-4512-8e2b-23421854508a',
                   get_data_from_file("film_id_5a5f31ab-d212-4512-8e2b-23421854508a.json"), 200),
                  ('c8cb8aa5-926c-4180-81cb-404e2be58a2c', None, 404)
                  ]