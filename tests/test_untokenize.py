import pytest
from pybo.untokenize import *

def test_untokenize_clean_text():
    tokenized_text = "སྒྲ་བསྒྱུར་ མར་པ་ ལོ་ ཙྪའི་ རྣམ་པར་ ཐར་པ་ མཐོང་བ་ དོན་ཡོད་ བཞུགས་ སོ །། ན་མོ་གུ་རུ་ དེ་ཝ་ཌཱ་ཀི་ནི ། "
    tokens = pre_processing(tokenized_text)
    detokenized_text = assemble(tokens)
    expected_text = "སྒྲ་བསྒྱུར་མར་པ་ལོ་ཙྪའི་རྣམ་པར་ཐར་པ་མཐོང་བ་དོན་ཡོད་བཞུགས་སོ།།ན་མོ་གུ་རུ་དེ་ཝ་ཌཱ་ཀི་ནི།"
    assert expected_text == detokenized_text

def test_untokenize_single_tagged_text():
    tokenized_text = "སྒྲ་བསྒྱུར་/NO_POS མར་པ་/NO_POS ལོ་/NO_POS ཙྪའི་/NO_POS རྣམ་པར་/NO_POS ཐར་པ་/NO_POS མཐོང་བ་/NO_POS དོན་ཡོད་/NO_POS བཞུགས་/NO_POS སོ/NO_POS །།/NO_POS ན་མོ་གུ་རུ་/NO_POS དེ་ཝ་ཌཱ་ཀི་ནི/NO_POS །/NO_POS "
    tokens = pre_processing(tokenized_text)
    detokenized_text = assemble(tokens)
    expected_text = "སྒྲ་བསྒྱུར་མར་པ་ལོ་ཙྪའི་རྣམ་པར་ཐར་པ་མཐོང་བ་དོན་ཡོད་བཞུགས་སོ།།ན་མོ་གུ་རུ་དེ་ཝ་ཌཱ་ཀི་ནི།"
    assert expected_text == detokenized_text

def test_untokenize_multi_tagged_text():
    tokenized_text = "ལས་//// ཞེས་པ་//PART/ཞེས་པ་/ ནི་//PART/ནི་/ ལས་//// བྱེད་པ//VERB/བྱེད་པ་/"
    tokens = pre_processing(tokenized_text)
    detokenized_text = assemble(tokens)
    expected_text = "ལས་ཞེས་པ་ནི་ལས་བྱེད་པ"
    assert expected_text == detokenized_text