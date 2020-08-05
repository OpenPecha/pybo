from pathlib import Path

import pytest

from pybo.monlam2wordlist import (
    csv_loader,
    get_definition_list,
    get_pos_list,
    get_tag_list,
    monlam2wordlist,
    parse_attrs,
)

testcases_ids = ("one_pos_one_sense", "one_pos_multi_senses", "multi_pos_multi_senses")

# monlam-result-col, pos-list, definition-list, tag-list, sense-list, example-list
parser_to_try = (
    (
        "མིང་ཚིག ༡ཀ། ཀཀ། ཁཁ། གག།",
        [("མིང་ཚིག", "༡ཀ། ཀཀ། ཁཁ། གག།")],
        [("མིང་ཚིག", "༡ཀ། ཀཀ། ཁཁ། གག།")],
        [("མིང་ཚིག", "༡ཀ།", "ཀཀ། ཁཁ། གག།")],
    ),
    (
        "མིང་ཚིག 1. ༡ཀ། ཀཀ། 2. ༡ཀ། ཁཁ། 3. གག།",
        [("མིང་ཚིག", "༡ཀ། ཀཀ། 2. ༡ཀ། ཁཁ། 3. གག།")],
        [("མིང་ཚིག", "༡ཀ། ཀཀ།"), ("མིང་ཚིག", "༡ཀ། ཁཁ།"), ("མིང་ཚིག", "གག།")],
        [("མིང་ཚིག", "༡ཀ།", "ཀཀ།"), ("མིང་ཚིག", "༡ཀ།", "ཁཁ།"), ("མིང་ཚིག", "", "གག།")],
    ),
    (
        "མིང་ཚིག 1. ༡ཀ། ཀཀ། 2. ཁཁ། བྱེད་ཚིག 1. ཀཀ། 2. ༡ཀ། ཁཁ། གྲོགས་ཚིག ༡ཀ། ཀཀ། ཁཁ། བྱེད་ཚིག ཀཀ། ཁཁ།",
        [
            ("མིང་ཚིག", "༡ཀ། ཀཀ། 2. ཁཁ།"),
            ("བྱེད་ཚིག", "ཀཀ། 2. ༡ཀ། ཁཁ།"),
            ("གྲོགས་ཚིག", "༡ཀ། ཀཀ། ཁཁ།"),
            ("བྱེད་ཚིག", "ཀཀ། ཁཁ།"),
        ],
        [
            ("མིང་ཚིག", "༡ཀ། ཀཀ།"),
            ("མིང་ཚིག", "ཁཁ།"),
            ("བྱེད་ཚིག", "ཀཀ།"),
            ("བྱེད་ཚིག", "༡ཀ། ཁཁ།"),
            ("གྲོགས་ཚིག", "༡ཀ། ཀཀ། ཁཁ།"),
            ("བྱེད་ཚིག", "ཀཀ། ཁཁ།"),
        ],
        [
            ("མིང་ཚིག", "༡ཀ།", "ཀཀ།"),
            ("མིང་ཚིག", "", "ཁཁ།"),
            ("བྱེད་ཚིག", "", "ཀཀ།"),
            ("བྱེད་ཚིག", "༡ཀ།", "ཁཁ།"),
            ("གྲོགས་ཚིག", "༡ཀ།", "ཀཀ། ཁཁ།"),
            ("བྱེད་ཚིག", "", "ཀཀ། ཁཁ།"),
        ],
    ),
)


@pytest.fixture(params=parser_to_try, ids=testcases_ids)
def parser_testcase(request):
    return request.param


def test_get_pos_list(parser_testcase):
    monlam_result_col, pos_expected, *_ = parser_testcase
    assert get_pos_list(monlam_result_col) == pos_expected


def test_get_definition_list(parser_testcase):
    _, pos_list, definition_expected, *_ = parser_testcase
    assert get_definition_list(pos_list) == definition_expected


def test_get_tag_list(parser_testcase):
    _, _, definition_list, tag_expected = parser_testcase
    assert get_tag_list(definition_list) == tag_expected


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


# def test_monlam2wordlist(a_testcase):
#     monlam_rows, expected_rows = a_testcase
#     wordlists = monlam2wordlist(monlam_rows)
#     print(wordlists)
