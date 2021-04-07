from pathlib import Path
from re import T

from bordr import rdr as r
from botok.tokenizers.wordtokenizer import WordTokenizer

from pybo.rdr.rdr_2_replace_matcher import rdr_2_replace_matcher
from pybo.hfr_cqlr_converter import cqlr2hfr

from pybo.segmentation_rule.make_rule import *


HOME = Path.home()
DIALECT_PACK_DIR = HOME / "Documents" / "pybo" / "dialect_packs"
DEFAULT_DPACK = "general"


def get_pybo_segmentation(sample_text):
    """
    Tokenize the sample text using botok token
    """
    wt = WordTokenizer()
    tokens = wt.tokenize(sample_text)
    segmented_sample_text = ''
    for token in tokens:
        token_with_tag = f'{token.text} '
        segmented_sample_text += token_with_tag
    segmented_sample_text = segmented_sample_text.replace('\n ', '\n')
    segmented_sample_text = segmented_sample_text.replace('  ', ' ')
    return segmented_sample_text

def post_process_human_data(human_data):
    human_data = human_data.replace('།  །', '།།')
    human_data = human_data.replace('  ', ' ')
    return human_data

def get_toks(seg_str):
    tokens = seg_str.split(' ')
    return tokens

def get_training_line(human_toks, pybo_toks):
    training_line = ''
    while True:
        human_tok = human_toks[0]
        cur_tok = ''
        for tok_walker, pybo_tok in enumerate(pybo_toks):
            if pybo_tok == human_tok:
                training_line += f'{pybo_tok}/U '
                del pybo_toks[tok_walker]
                break
            elif pybo_tok in human_tok:
                cur_tok += pybo_tok
                if cur_tok == human_tok:
                    training_line += f'{pybo_tok}/I '
                    pybo_toks = pybo_toks[tok_walker+1:]
                    break
                elif tok_walker == 0:
                    training_line += f'{pybo_tok}/B '
                else:
                    training_line += f'{pybo_tok}/I '
            elif human_tok in pybo_tok:
                cur_tok = ''
                training_line += f'{pybo_tok}/S '
                del pybo_toks[tok_walker]
                # human_toks = human_toks[1:]
                break
            else:
                pybo_toks = pybo_toks[tok_walker:]
                break
        human_toks = human_toks[1:]
        if not human_toks:
            break
    return training_line

def get_training_data(input_path, human_data):
    input_file_name = input_path.stem
    pybo_data = get_pybo_segmentation(input_path.read_text(encoding='utf-8-sig'))
    (input_path.parent / f'{input_file_name}_pybo_data.txt').write_text(pybo_data, encoding='utf-8')
    human_lines = human_data.splitlines()
    pybo_lines = pybo_data.splitlines()
    training_data = ''
    for human_line, pybo_line in zip(human_lines, pybo_lines):
        human_toks = get_toks(human_line)
        pybo_toks = get_toks(pybo_line)
        training_data += get_training_line(human_toks, pybo_toks) + '\n'
    return training_data

def get_split_suggestions(training_data):
    split_suggestions = [split_token[:-2] for split_token in re.findall('\S+/S', training_data)]
    return list(set(split_suggestions))

def get_merge_suggestions(training_data):
    merge_suggestions = [merge_suggestion for merge_suggestion,_ in re.findall('(\S+/B (\S+/I )+)', training_data)]
    return list(set(merge_suggestions))

def parse_merge_suggestion(merge_suggestion):
    merge_suggestion_tokens = [token[:-2] for token in merge_suggestion.split(' ') if token]
    return merge_suggestion_tokens

def get_counter_merge_suggestion(merge_suggestion_tokens):
    counter_merge_suggestion = ' '.join(merge_suggestion_tokens)
    if merge_suggestion_tokens[-1][-1] == '་':
        counter_merge_suggestion += " "
    return counter_merge_suggestion
    
def get_remove_word_candidate(split_suggestions, human_data):
    remove_word_candidate = []
    for spilt_suggestion_token in split_suggestions:
        if spilt_suggestion_token not in human_data:
            remove_word_candidate.append(spilt_suggestion_token)
    return remove_word_candidate

def get_new_word_candidate(merge_suggestions, human_data):
    new_word_candidate = []
    for merge_suggestion in merge_suggestions:
        merge_suggestion_tokens = parse_merge_suggestion(merge_suggestion)
        counter_merge_suggestion = " " + get_counter_merge_suggestion(merge_suggestion_tokens)
        if counter_merge_suggestion not in human_data:
            new_word_candidate.append(''.join(merge_suggestion_tokens))
    return new_word_candidate

def filter_seg_errors(training_data, human_data):
    new_word_candidate = []
    new_remove_word_candidate = []
    split_suggestions = get_split_suggestions(training_data)
    merge_suggestions = get_merge_suggestions(training_data)
    new_word_candidate = get_new_word_candidate(merge_suggestions, human_data)  
    new_remove_word_candidate = get_remove_word_candidate(split_suggestions, human_data)
    return new_word_candidate, new_remove_word_candidate

def rdr_postprocess(file_path):
    suffixes = [".DICT", ".INIT", ".RAW", ".RDR", ".sDict"]
    for s in suffixes:
        Path(file_path.parent / (file_path.name + s)).unlink()

def remove_duplicate_word(word_list):
    return list(set(word_list))

def add_word_2_adjustment(words_2_add, input_file_name,dialect_pack_name, type='words'):
    old_word_list = []
    word_list_path = (DIALECT_PACK_DIR / dialect_pack_name / "adjustments" / type / f'{input_file_name}.tsv')
    if word_list_path.is_file():
        old_word_list = [old_word for old_word in word_list_path.read_text(encoding='utf-8-sig').splitlines() if old_word]
    new_word_list = old_word_list + words_2_add
    new_word_list = remove_duplicate_word(new_word_list)
    new_words = '\n'.join(new_word_list)
    word_list_path.write_text(new_words, encoding='utf-8-sig')
    print(f'[INFO]: New {type} added to adjustment {type} list..')

def get_bilou_rules(training_data_path):
    log = r(str(training_data_path), mode="train", verbose=True)
    print('[INFO]: RDR TRAINING COMPLETED..')
    rdr_rules = Path(f"{training_data_path}.RDR").read_text(
        encoding="utf-8-sig"
    )
    bilou_rules = rdr_2_replace_matcher(rdr_rules).splitlines()
    bilou_rules = list(set(bilou_rules))
    return bilou_rules

def convert_bilou_rules(bilou_rules, training_init, human_data):
    new_cql_rules = []
    for bilou_rule in bilou_rules:
        tokens_info, index, operator, conclusion = parse_rule(bilou_rule)
        tokens = get_tokens(tokens_info)
        tokens_of_interest = get_match_tokens(tokens, training_init)
        new_cql_rules += get_new_rule(tokens_of_interest, int(index), conclusion, human_data)
    new_cql_rules = list(set(new_cql_rules))
    return new_cql_rules

def extract_seg_rule(input_path, dialect_pack_name=DEFAULT_DPACK, type='cql', no_epochs = 3):
    new_word_list = []
    new_remove_word_list = []
    input_file_name = input_path.stem
    number_of_segmentation = 1
    human_data = (input_path.parent / f'{input_file_name}_hd.txt').read_text(encoding='utf-8-sig')
    human_data = post_process_human_data(human_data)
    while True:
        training_data = get_training_data(input_path, human_data)
        print(f'[INFO]: SEGMENTATION PHASE {number_of_segmentation} COMPLETED..')
        new_word_list, new_remove_word_list = filter_seg_errors(training_data, human_data)
        print('[INFO]: FILTER SEGMENTATION ERROR COMPLETED..')
        if new_word_list:
            add_word_2_adjustment(new_word_list, input_file_name, dialect_pack_name, type='words')
        if new_remove_word_list:
            add_word_2_adjustment(new_remove_word_list, input_file_name, dialect_pack_name, type='remove')
        training_data = get_training_data(input_path, human_data)
        word_list, remove_word_list = filter_seg_errors(training_data, human_data)
        new_remove_word_list = [remove_word for remove_word in remove_word_list if remove_word not in new_remove_word_list]
        new_word_list = [word for word in word_list if word not in new_word_list]
        number_of_segmentation += 1
        if (not new_word_list and not new_remove_word_list) or number_of_segmentation > no_epochs:
            break
    training_data_path = (input_path.parent / f'{input_file_name}_tr_data.txt')
    training_data_path.write_text(training_data, encoding='utf-8')
    bilou_rules = get_bilou_rules(training_data_path)
    new_cql_rules = []
    training_init = (input_path.parent / f'{training_data_path.name}.INIT').read_text(encoding='utf-8-sig')
    new_cql_rules = convert_bilou_rules(bilou_rules, training_init, human_data)
    new_cql_rules = "\n".join(new_cql_rules)
    rdr_postprocess(training_data_path)
    if type != 'cql':
        new_cql_rules = cqlr2hfr(new_cql_rules)
    return new_cql_rules