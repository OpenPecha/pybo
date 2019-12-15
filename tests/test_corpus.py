from pathlib import Path
from textwrap import dedent

from pybo import *


def test_parse_manually_corrected():
    dump = Path(__file__).parent / "resources/step2/manually_corrected.txt"
    dump = dump.read_text(encoding="utf-8-sig")
    data = extract_new_entries(dump, Path(__file__).parent / "resources/main")
    assert data == dedent("""\
            # form	pos	lemma	sense	freq
            །_		།		12
            །_	PUNCT			
            ཏུ་	PART	དུ་		
            ཐོབ་པ་	VERB			
            ཐོབ་པ་	VERB	ཐོབ་		
            ཕུན་སུམ་ཚོགས་	ADJ			
            བཀྲ་ཤིས་	NOUN			
            བཀྲ་ཤིས་བདེ་ལེགས་	NOUN			
            བདེ་བ་	NOUN			
            བདེ་ལེགས་	NOUN			
            ར་	PART			
            ར་	PART	ལ་		
            རྟག་	NOUN			
            རྟག་	NOUN	རྟག་པ་		
            ཤོག་	AUX			
            ཤོག་	AUXr			""")
