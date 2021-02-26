import pytest

from pybo.hfr_cqlr_converter import cqlr2hfr, hfr2cqlr

@pytest.fixture(scope="module")
def cqlr():
    return (
        '["ལ་ལ་"] ["ལ་ལ་"]	1	=	[pos="PART"]'
        '["ལ་ལ་"] ["ལ་ལ་"]	2	=	[pos="PART"]'
        '["ལ་ལ་"] ["ལ་ལ་"]	1-2	::	[pos="NOUN"] [pos="PART"]'
        '["ལ་"] ["ལ་"] ["ལ་ལ་"]	3-2	::	[pos="PART"] [pos="PART"]'
        '["ལ་"] ["ལ་"] ["ལ་"] ["ལ་"]	2	+	[pos="DET"]'
    )


@pytest.fixture(scope="module")
def hfr():
    return (
        '༺"ལ་ལ་"༻ ༺"ལ་ལ་"༻	1	=	༺གཤིས=རོགས༻'
        '༺"ལ་ལ་"༻ ༺"ལ་ལ་"༻	2	=	༺གཤིས=རོགས༻'
        '༺"ལ་ལ་"༻ ༺"ལ་ལ་"༻	1-2	::	༺གཤིས=མིང༻ ༺གཤིས=རོགས༻'
        '༺"ལ་"༻ ༺"ལ་"༻ ༺"ལ་ལ་"༻	3-2	::	༺གཤིས=རོགས༻ ༺གཤིས=རོགས༻'
        '༺"ལ་"༻ ༺"ལ་"༻ ༺"ལ་"༻ ༺"ལ་"༻	2	+	༺གཤིས=ངེས༻'
    )


def test_cql2hfr(cqlr, hfr):
    hfr_result = cqlr2hfr(cqlr)
    print(hfr_result)
    assert hfr_result == hfr
    print("Test pass..")


def test_hfr2cql(hfr, cqlr):
    cql_result = hfr2cqlr(hfr)
    assert cql_result == cqlr
    print("Test pass..")
