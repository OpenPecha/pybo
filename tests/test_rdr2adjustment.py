from pathlib import Path
from textwrap import dedent

from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher


def test_suffix_bug():
    dump = Path("tests/resources/rdr_rules.txt").read_text()
    rules = rdr_2_replace_matcher(dump)
    expected = dedent(
        """\
            [pos="DET" & text="དག"] [pos="PART"]	1	=	[pos="VERB"]
            [pos="PART" & text="ས"] [pos="PART"]	1	=	[pos="ADP"]
            [pos="PUNCT"] [pos="PART" & text="ས་"]	2	=	[pos="ADP"]
            [pos="PART"] [pos="PART" & text="ས་"]	2	=	[pos="ADP"]
            [pos="PART" & text="མི"] [pos="PART" & text="ས་"]	2	=	[pos="PART"]
            [text="བྷ་"] [pos="PART"]	2	=	[pos="ADP"]
            [pos="PART" & text="ས་"] [text="ལ་"]	1	=	[pos="ADP"]
            [text="ལ"] [pos="PART" & text="ས་"] [text="ལ་"]	2	=	[pos="PART"]
            [pos="PART"] [text="སྟེངས་"]	1	=	[pos="ADP"]
            [pos="PART" & text="ར"] [text="འི་"]	1	=	[pos="ADP"]
            [pos="VERB"] [text=".*མ"]	1	=	[pos="NOUN"]
            [pos="VERB"] [text=".*ན"]	1	=	[pos="OOV"]
            [pos="VERB"] [] [text="བོད་སྐད་"]	1	=	[pos="NON_WORD"]
            [pos="VERB"] [text="ཡིག་"]	1	=	[pos="NON_WORD"]
            [pos="VERB"] [] [text=".*ཕྱོགས་"]	1	=	[pos="NOUN"]
            [pos="VERB"] [pos="NUM"] [pos="NUM"]	1	=	[pos="NOUN"]
            [text="དཔེར་ན་"] [pos="VERB"]	2	=	[pos="NOUN"]
            [text="།_"] [pos="VERB"] [text="ལ་སོགས་པ་"]	2	=	[pos="NOUN"]
            [pos="VERB"] [text=".*སོ"]	1	=	[pos="OOV"]
            [pos="VERB"] [] [text=".*སྐྱེས་"]	1	=	[pos="OOV"]
            [pos="VERB"] [pos="NON_WORD"]	1	=	[pos="OOV"]
            [pos="VERB"] [] [text=".*ཆད་"]	1	=	[pos="ADV"]
            [pos="NOUN"] [pos="SCONJ"]	2	=	[pos="ADP"]
            [pos="DET"] [pos="SCONJ"]	2	=	[pos="ADP"]"""
    )
    assert rules == expected
