from pathlib import Path

import pytest

from pybo.utils.monlam2wordlist import csv_loader, monlan2wordlist, parse_attrs

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

testcases_ids = ("one_pos_one_sense", "one_pos_multi_sense", "multi_pos_multi_sense")


@pytest.fixture(params=testcases_to_try, ids=testcases_ids)
def a_testcase(request):
    return request.param


def test_monlam2wordlist(a_testcase):
    monlam_rows, expected_rows = a_testcase
    wordlists = monlan2wordlist(monlam_rows)
    print(wordlists)
