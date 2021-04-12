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


def test_construct_training_line():
    human_toks = ["སྒྲ་བསྒྱུར་", "མར་པ་", "ལོ་ཙྪ", "འི་", "རྣམ་པར་", "ཐར་པ་", "མཐོང་བ་", "དོན་ཡོད་", "བཞུགས་", "སོ", "།།", "ན་མོ་གུ་རུ་", "དེ་ཝ་ཌཱ་ཀི་ནི", "།"]
    pybo_toks = ["སྒྲ་", "བསྒྱུར་", "མར་པ་", "ལོ་", "ཙྪའི་", "རྣམ་པ", "ར་", "ཐར་པ་", "མཐོང་བ་", "དོན་ཡོད་", "བཞུགས་", "སོ", "།།", "ན་མོ་", "གུ་རུ་", "དེ་ཝ་", "ཌཱ་ཀི་", "ནི", "།"]
    expected_training_line = 'སྒྲ་/B བསྒྱུར་/I མར་པ་/U ལོ་/B ཙྪའི་/S རྣམ་པ/B ར་/I ཐར་པ་/U མཐོང་བ་/U དོན་ཡོད་/U བཞུགས་/U སོ/U །།/U ན་མོ་/B གུ་རུ་/I དེ་ཝ་/B ཌཱ་ཀི་/I ནི/I །/U '
    assert expected_training_line == get_bilou_tag_line(human_toks, pybo_toks)

def test_get_new_word_candidate():
    merge_suggestions = ["སྒྲ་\B བསྒྱུར་\I", "དོན་\B ཡོད་\I"]
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ ། མཐོང་བ་ དོན་ ཡོད་ བཞུགས་ སོ །"
    expected_new_words = ["སྒྲ་བསྒྱུར་"]
    assert expected_new_words == get_new_word_candidates(merge_suggestions, human_data)

def test_get_remove_word_candidate():
    split_suggestions = ["སྒྲ་བསྒྱུར་", "དོན་ཡོད་", "མཐོང་བ་"]
    human_data = "སྒྲ་ བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་ བ་ དོན་ཡོད་ བཞུགས་ སོ ། མཐོང་ བ་ དོན་ ཡོད་ བཞུགས་ སོ །"
    expected_remove_words = ["སྒྲ་བསྒྱུར་", "མཐོང་བ་"]
    assert expected_remove_words == get_remove_word_candidates(split_suggestions, human_data)

def test_false_positive_merge():
    tokens_in_rule = ['["ང་"]', '["ཁོང་"]', '["ཅན་"]', '["དུ་"]', '["མི་"]']
    index = 2
    human_data = "སྒོམ་ བྱེད་ ཀྱིན་ ཡོད་ འདུག་པ ས ། ང་ ཁོང་ ཅན་ དུ་ མི་ འགྲོ ཁྱེད་རང་ ང འི་ ཕྱི་ ལ་ འགྲོ་ ན་ གསེར་ མཉམ་ དུ་ བྱེད །"
    assert True == is_false_positive_merge(tokens_in_rule, index, human_data)

def test_true_positive_merge():
    tokens_in_rule = ['["ཁྱོད་"]', '["ཁོང་"]', '["ཅན་"]', '["བཏང་"]', '["དགོས་"]']
    index = 2
    human_data = "མ་རྒྱུད་ ཀྱི་ བདག་པོ་ གཅིག་ བཞུགས་ ཤིང་ ཡོད་པ ས་ ཁྱོད་ ཁོང་ཅན་ བཏང་ དགོས་ གསུངས །"
    assert False == is_false_positive_merge(tokens_in_rule, index, human_data)

def test_true_positive_split():
    tokens_in_rule = ['["ང་"]', '["ཁོང་ཅན་"]', '["དུ་"]', '["མི་"]']
    index = 2
    counter_split_suggestion = ' ཁོང་ ཅན་ '
    human_data = "སྒོམ་ བྱེད་ ཀྱིན་ ཡོད་ འདུག་པ ས ། ང་ ཁོང་ ཅན་ དུ་ མི་ འགྲོ ཁྱེད་རང་ ང འི་ ཕྱི་ ལ་ འགྲོ་ ན་ གསེར་ མཉམ་ དུ་ བྱེད །"
    assert False == is_false_positive_split(tokens_in_rule, index, counter_split_suggestion, human_data)

def test_false_positive_split():
    tokens_in_rule = ['["ཁྱོད་"]', '["ཁོང་ཅན་"]', '["བཏང་"]', '["དགོས་"]']
    index = 2
    counter_split_suggestion = ' ཁོང་ ཅན་ '
    human_data = "མ་རྒྱུད་ ཀྱི་ བདག་པོ་ གཅིག་ བཞུགས་ ཤིང་ ཡོད་པ ས་ ཁྱོད་ ཁོང་ཅན་ བཏང་ དགོས་ གསུངས །"
    assert True == is_false_positive_split(tokens_in_rule, index, counter_split_suggestion, human_data)

def test_invalid_split_rule():
    tokens_info = '["སྒྲ་བསྒྱུར་"] ["མར་པ་"]'
    index_info = '2-1'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །།"
    assert True == is_invalid_split(tokens_info, index_info, human_data)

def test_valid_split_rule():
    tokens_info = '["སྒྲ་"] ["བསྒྱུར་"] ["མཐོང་བ་"]'
    index_info = '3-1'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །། སྒྲ་ བསྒྱུར་ མཐོང་ བ་ དོན་ ཡོད་ བཞུགས་ སོ"
    assert False == is_invalid_split(tokens_info, index_info, human_data)

def test_invalid_merge_rule():
    tokens_info = '["སྒྲ་བསྒྱུར་"] ["མར་"] ["པ་"]'
    index_info = '2'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །།"
    assert True == is_invalid_merge(tokens_info, index_info, human_data)

def test_valid_merge_rule():
    tokens_info = '["ཐར་པ་"] ["མཐོང་"] ["བ་"]'
    index_info = '2'
    human_data = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ཙྪ འི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །། སྒྲ་ བསྒྱུར་ མཐོང་ བ་ དོན་ ཡོད་ བཞུགས་ སོ"
    assert False == is_invalid_merge(tokens_info, index_info, human_data)


if __name__ == "__main__":
    # input_path = Path('./tests/corpus1/corpus1.txt')
    input_path = Path('./tests/marpa/marpa.txt')
    rules = extract_seg_rule(input_path, type='cql')
    (input_path.parent / f'{input_path.stem}_rules.txt').write_text(rules, encoding='utf-8')