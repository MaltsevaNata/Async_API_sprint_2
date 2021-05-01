import pytest

from pathlib import Path

parent_dir = Path(__file__).parents[1]
files_dir = parent_dir.joinpath("expected_data", "films")

# Format of parameters: (query_params, expected_data_file, status, page_size)
default_params = [({}, files_dir.joinpath("film_list_default.json"), 200, 50)]

sort_params = [({"sort": "imdb_rating"}, files_dir.joinpath("film_list_default.json"), 200, 50),
               ({"sort": "-imdb_rating"}, files_dir.joinpath("film_list_desc_sorted.json"), 200, 50),
               ({"sort": "rating"}, None, 422, None)]

page_num_params = [({"page_number": 0}, files_dir.joinpath("film_list_default.json"), 200, 50),
                   ({"page_number": 15}, files_dir.joinpath("film_list_page_number_15.json"), 200, 50),
                   ({"page_number": 19}, files_dir.joinpath("film_list_page_number_19.json"), 200, 49),
                   ({"page_number": "two"}, None, 422, None),
                   pytest.param({"page_number": 20}, None, 204, None,
                                marks=pytest.mark.xfail(reason="Fix response status 200->204")),
                   pytest.param({"page_number": -1}, None, 422, None,
                                marks=pytest.mark.xfail(reason="Fix response status 500->422"))]
