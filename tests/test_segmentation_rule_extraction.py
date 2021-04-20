import pytest
import re

from pybo.segmentation_rule.make_rule import *
from pybo.segmentation_rule.pipeline import *

@pytest.fixture(scope="module")
def human_data():
    return "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །  ། ན་མོ་གུ་རུ་ དེ་ཝ་ཌཱ་ཀི་ནི །  སྔོན་སྦྱངས་ ཐུགས་བསྐྱེད་ སྨོན་ལམ་ དུས་ བབས་ ལྷག་བསམ་ གྲུ་གཟིངས་ ནང་ དུ་ ལུས་སྲོག་ མ་ ཆགས་ འགྲོ་དོན་ སྦྱོར་བ་ མཆོག་ གིས་ རབ་ ཞུགས་ ནས །"

@pytest.fixture(scope="module")
def source_data():
    return "སྒྲ་བསྒྱུར་མར་པ་ལོ་ཙྪའི་རྣམ་པར་ཐར་པ་མཐོང་བ་དོན་ཡོད་བཞུགས་སོ།།ན་མོ་གུ་རུ་དེ་ཝ་ཌཱ་ཀི་ནི།སྔོན་སྦྱངས་ཐུགས་བསྐྱེད་སྨོན་ལམ་དུས་བབས་ལྷག་བསམ་གྲུ་གཟིངས་ནང་དུ་ལུས་སྲོག་མ་ཆགས་འགྲོ་དོན་སྦྱོར་བ་མཆོག་གིས་རབ་ཞུགས་ནས།"


def test_postprocessing_human_data(human_data):
    expected_human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །། ན་མོ་གུ་རུ་ དེ་ཝ་ཌཱ་ཀི་ནི ། སྔོན་སྦྱངས་ ཐུགས་བསྐྱེད་ སྨོན་ལམ་ དུས་ བབས་ ལྷག་བསམ་ གྲུ་གཟིངས་ ནང་ དུ་ ལུས་སྲོག་ མ་ ཆགས་ འགྲོ་དོན་ སྦྱོར་བ་ མཆོག་ གིས་ རབ་ ཞུགས་ ནས །"
    assert expected_human_data == post_process_human_data(human_data)


def test_construct_bilou_tag_line():
    human_toks = ["སྒྲ་བསྒྱུར་", "མར་པ་", "ལོ་ཙྪ", "འི་", "རྣམ་པར་", "ཐར་པ་", "མཐོང་བ་", "དོན་ཡོད་", "བཞུགས་", "སོ", "།།", "ན་མོ་གུ་རུ་", "དེ་ཝ་ཌཱ་ཀི་ནི", "།", "རྣམས་", "ལས་", "དམ་ཆོས་", "ནོར་བུ་", "དགོས་འདོད་", "ཆར་འབབས་", "བླངས་", "ནས་", "ནི", "།།", "གི", "ས་", "བསྐྱོད་", "ཕུ་ལ་ཧ་རི་"]
    botok_toks = ["སྒྲ་<NO_POS>", "བསྒྱུར་<NO_POS>", "མར་པ་<NO_POS>", "ལོ་<NO_POS>", "ཙྪའི་<NO_POS>", "རྣམ་པ<NO_POS>", "ར་<NO_POS>", "ཐར་པ་<NO_POS>", "མཐོང་བ་<NO_POS>", "དོན་<NO_POS>", "ཡོད་<NO_POS>", "བཞུགས་<NO_POS>", "སོ<NO_POS>", "།།<NO_POS>", "ན་མོ་<NO_POS>", "གུ་རུ་<NO_POS>", "དེ་ཝ་<NO_POS>", "ཌཱ་ཀི་<NO_POS>", "ནི<NO_POS>", "།<NO_POS>", "རྣམས་<DET>", "ལས་དམ་<NO_POS>", "ཆོས་ནོར་<NO_POS>", "བུ་<NOUN>", "དགོས་འདོད་<NOUN>", "ཆ<NOUN>", "ར་<PART>", "འབབས་<NON_WORD>", "བླངས་<VERB>", "ནས་<PART>", "ནི<PART>", "།།<PUNCT>", "གིས་<NON_WORD>", "བསྐྱོད་<VERB>", "ཕུ་ལ་ཧ་རི་<NO_POS>"]
    expected_bilou_line = 'སྒྲ་<NO_POS>/B བསྒྱུར་<NO_POS>/I མར་པ་<NO_POS>/U ལོ་<NO_POS>/B ཙྪའི་<NO_POS>/S རྣམ་པ<NO_POS>/B ར་<NO_POS>/I ཐར་པ་<NO_POS>/U མཐོང་བ་<NO_POS>/U དོན་<NO_POS>/B ཡོད་<NO_POS>/I བཞུགས་<NO_POS>/U སོ<NO_POS>/U །།<NO_POS>/U ན་མོ་<NO_POS>/B གུ་རུ་<NO_POS>/I དེ་ཝ་<NO_POS>/B ཌཱ་ཀི་<NO_POS>/I ནི<NO_POS>/I །<NO_POS>/U རྣམས་<DET>/U ལས་དམ་<NO_POS>/S ཆོས་ནོར་<NO_POS>/S བུ་<NOUN>/I དགོས་འདོད་<NOUN>/U ཆ<NOUN>/B ར་<PART>/I འབབས་<NON_WORD>/I བླངས་<VERB>/U ནས་<PART>/U ནི<PART>/U །།<PUNCT>/U གིས་<NON_WORD>/S བསྐྱོད་<VERB>/U ཕུ་ལ་ཧ་རི་<NO_POS>/U '
    assert expected_bilou_line == get_bilou_tag_line(human_toks, botok_toks)

def test_get_new_word_candidate():
    merge_suggestions = ["སྒྲ་<NO_POS>/B བསྒྱུར་<NO_POS>/I", "དོན་<NO_POS>\B ཡོད་<NO_POS>\I"]
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ ། མཐོང་བ་ དོན་ ཡོད་ བཞུགས་ སོ །"
    expected_new_words = ["སྒྲ་བསྒྱུར་"]
    assert expected_new_words == get_new_word_candidates(merge_suggestions, human_data)

def test_get_remove_word_candidate():
    split_suggestions = ["སྒྲ་བསྒྱུར་<NO_POS>", "དོན་ཡོད་<NO_POS>", "མཐོང་བ་<NO_POS>"]
    human_data = " སྒྲ་ བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་ བ་ དོན་ཡོད་ བཞུགས་ སོ ། མཐོང་ བ་ དོན་ ཡོད་ བཞུགས་ སོ །"
    expected_remove_words = ["སྒྲ་བསྒྱུར་", "མཐོང་བ་"]
    assert expected_remove_words == get_remove_word_candidates(split_suggestions, human_data)

def test_false_positive_merge():
    tokens_in_rule = ['[text="ང་"]', '[text="ཁོང་"]', '[text="ཅན་"]', '[text="དུ་"]', '[text="མི་"]']
    index = 2
    human_data = "སྒོམ་ བྱེད་ ཀྱིན་ ཡོད་ འདུག་པ ས ། ང་ ཁོང་ ཅན་ དུ་ མི་ འགྲོ ཁྱེད་རང་ ང འི་ ཕྱི་ ལ་ འགྲོ་ ན་ གསེར་ མཉམ་ དུ་ བྱེད །"
    assert True == is_false_positive_merge(tokens_in_rule, index, human_data)

def test_true_positive_merge():
    tokens_in_rule = ['[text="ཁྱོད་"]', '[text="ཁོང་"]', '[text="ཅན་"]', '[text="བཏང་"]', '[text="དགོས་"]']
    index = 2
    human_data = "མ་རྒྱུད་ ཀྱི་ བདག་པོ་ གཅིག་ བཞུགས་ ཤིང་ ཡོད་པ ས་ ཁྱོད་ ཁོང་ཅན་ བཏང་ དགོས་ གསུངས །"
    assert False == is_false_positive_merge(tokens_in_rule, index, human_data)

def test_true_positive_split():
    tokens_in_rule = ['[text="ང་"]', '[text="ཁོང་ཅན་"]', '[text="དུ་"]', '[text="མི་"]']
    index = 2
    counter_split_suggestion = ' ཁོང་ ཅན་ '
    human_data = "སྒོམ་ བྱེད་ ཀྱིན་ ཡོད་ འདུག་པ ས ། ང་ ཁོང་ ཅན་ དུ་ མི་ འགྲོ ཁྱེད་རང་ ང འི་ ཕྱི་ ལ་ འགྲོ་ ན་ གསེར་ མཉམ་ དུ་ བྱེད །"
    assert False == is_false_positive_split(tokens_in_rule, index, counter_split_suggestion, human_data)

def test_false_positive_split():
    tokens_in_rule = ['[text="ཁྱོད་"]', '[text="ཁོང་ཅན་"]', '[text="བཏང་"]', '[text="དགོས་"]']
    index = 2
    counter_split_suggestion = ' ཁོང་ ཅན་ '
    human_data = "མ་རྒྱུད་ ཀྱི་ བདག་པོ་ གཅིག་ བཞུགས་ ཤིང་ ཡོད་པ ས་ ཁྱོད་ ཁོང་ཅན་ བཏང་ དགོས་ གསུངས །"
    assert True == is_false_positive_split(tokens_in_rule, index, counter_split_suggestion, human_data)

def test_invalid_split_rule():
    tokens_info = '[text="སྒྲ་བསྒྱུར་"] [text="མར་པ་"]'
    index_info = '2-1'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །།"
    assert (True,0) == is_invalid_split(tokens_info, index_info, human_data)

def test_valid_split_rule():
    tokens_info = '[text="སྒྲ་"] [text="བསྒྱུར་"] [text="མཐོང་བ་"]'
    index_info = '3-1'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །། སྒྲ་ བསྒྱུར་ མཐོང་ བ་ དོན་ ཡོད་ བཞུགས་ སོ"
    assert (False,1) == is_invalid_split(tokens_info, index_info, human_data)

def test_invalid_merge_rule():
    tokens_info = '[text="སྒྲ་བསྒྱུར་"] [text="མར་"] [text="པ་"]'
    index_info = '2'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །།"
    assert True == is_invalid_merge(tokens_info, index_info, human_data)

def test_valid_merge_rule():
    tokens_info = '[text="ཐར་པ་"] [text="མཐོང་"] [text="བ་"]'
    index_info = '2'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །། སྒྲ་ བསྒྱུར་ མཐོང་ བ་ དོན་ ཡོད་ བཞུགས་ སོ"
    assert False == is_invalid_merge(tokens_info, index_info, human_data)


if __name__ == "__main__":
    # input_path = Path('./tests/corpus1/corpus1.txt')
    # input_path = Path('./tests/marpa/marpa.txt')
    input_path = Path('./tests/drokun_test/drokun_test.txt')
    rules = extract_seg_rule(input_path, type='cql')
    (input_path.parent / f'{input_path.stem}_rules.txt').write_text(rules, encoding='utf-8')