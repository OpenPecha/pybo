from pathlib import Path
from textwrap import dedent

from pybo import *


def test_parse_manually_corrected():
    dump = Path(__file__).parent / "resources/step2/manually_corrected.txt"
    dump = dump.read_text(encoding="utf-8-sig")
    words, data = generate_data(dump)
    assert data == """\
# form	pos	lemma	sense	freq
།_		།		12
།_	PUNCT			
བཀྲ་ཤིས་	NOUN			
བཀྲ་ཤིས་བདེ་ལེགས་	NOUN			
ཏུ་	PART	དུ་		
རྟག་	NOUN			
རྟག་	NOUN	རྟག་པ་		
ཐོབ་པ་	VERB			
ཐོབ་པ་	VERB	ཐོབ་		
བདེ་བ་	NOUN			
བདེ་ལེགས་	NOUN			
ཕུན་སུམ་ཚོགས་	ADJ			
ར་	PART			
ར་	PART	ལ་		
ཤོག་	AUX			"""
    assert words == """\
།_
བཀྲ་ཤིས་
བཀྲ་ཤིས་བདེ་ལེགས་
ཏུ་
རྟག་
ཐོབ་པ་
བདེ་བ་
བདེ་ལེགས་
ཕུན་སུམ་ཚོགས་
ར་
ཤོག་"""
