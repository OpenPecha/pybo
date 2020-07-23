from pybo.hfr_cqlr_converter import *
import pytest


@pytest.fixture(scope="module")
def cqlr():
    return (
        '[pos="DET" & སུ་] [pos="SCONJ"] 2   =   [pos="ADP"]'
        '["སུ་"] [pos="PRON"] ["ནས་" & pos="SCONJ"]   3   =   [pos="SCONJ"]'
    )


@pytest.fixture(scope="module")
def hfr():
    return (
        "༺གཤིས=ངེས ༈ སུ་༻ ༺གཤིས=ལྟོས༻ 2   =   ༺གཤིས=སྦྱོར༻"
        '༺"སུ་"༻ ༺གཤིས=ཚབ༻ ༺"ནས་" ༈ གཤིས=ལྟོས༻   3   =   ༺གཤིས=ལྟོས༻'
    )


def test_cql2hfr(cqlr, hfr):
    hfr_result = cql2hfr(cqlr)
    print(hfr_result)
    assert hfr_result == hfr
    print("Test pass..")


def test_hfr2cql(hfr, cqlr):
    cql_result = hfr2cql(hfr)
    assert cql_result == cqlr
    print("Test pass..")
