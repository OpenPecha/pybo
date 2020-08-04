from pathlib import Path

import pytest

from pybo.monlam2wordlist import csv_loader, get_pos_list, monlam2wordlist, parse_attrs

testcases_ids = ("one_pos_one_sense", "one_pos_multi_senses", "multi_pos_multi_senses")

pos_to_try = (
    ("མིང་ཚིག ཀཀ། ཁཁ། གག།", [("མིང་ཚིག", "ཀཀ། ཁཁ། གག།")]),
    ("མིང་ཚིག 1. ཀཀ། 2. ཁཁ། 3. གག།", [("མིང་ཚིག", "ཀཀ། 2. ཁཁ། 3. གག།")]),
    (
        "མིང་ཚིག 1. ཀཀ། 2. ཁཁ། མིང་ཚིག 1. ཀཀ། 2. ཁཁ། མིང་ཚིག ཀཀ། ཁཁ།",
        [("མིང་ཚིག", "ཀཀ། 2. ཁཁ།"), ("མིང་ཚིག", "ཀཀ། 2. ཁཁ།"), ("མིང་ཚིག", "ཀཀ། ཁཁ།")],
    ),
)


@pytest.fixture(params=pos_to_try, ids=testcases_ids)
def get_pos_list_testcase(request):
    return request.param


def test_get_pos_list(get_pos_list_testcase):
    monlam_result_col, expected = get_pos_list_testcase
    assert get_pos_list(monlam_result_col) == expected


data_path = Path("./tests/data/monlam2020/")
testcases_to_try = (
    (
        csv_loader(data_path / "one_pos_one_sense.csv"),
        csv_loader(data_path / "one_pos_one_sense_expected.csv"),
    ),
    (
        csv_loader(data_path / "one_pos_multi_sense.csv"),
        csv_loader(data_path / "one_pos_multi_sense_expected.csv"),
    ),
    (
        csv_loader(data_path / "multi_pos_multi_sense.csv"),
        csv_loader(data_path / "multi_pos_multi_sense_expected.csv"),
    ),
)


@pytest.fixture(params=testcases_to_try, ids=testcases_ids)
def a_testcase(request):
    return request.param


def test_monlam2wordlist(a_testcase):
    monlam_rows, expected_rows = a_testcase
    wordlists = monlam2wordlist(monlam_rows)
    print(wordlists)
