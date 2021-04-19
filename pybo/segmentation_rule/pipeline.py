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


def get_botok_segmentation(sample_text):
    """Tokenize sample text using botok tokenizer

    Args:
        sample_text (str): Input string that needs to be tokenize

    Returns:
        str: sample text with space between each tokens
    """
    wt = WordTokenizer()
    tokens = wt.tokenize(sample_text)
    segmented_sample_text = ''
    for token in tokens:
        token_text = token.text.replace(' ', '')
        if token.pos:
            token_pos = token.pos
        else:
            token_pos = token.chunk_type
        token_with_tag = f'{token_text}<{token_pos}> '
        if '\n' in token_with_tag:
            token_with_tag = token_with_tag.replace('\n', '')
            token_with_tag += '\n'
        segmented_sample_text += token_with_tag
    segmented_sample_text = segmented_sample_text.replace(' \n', '\n')
    return segmented_sample_text

def post_process_botok_segmented_data(segmented_text):
    """Remove unwanted space from segmented text

    Args:
        segmented_text (str): Botok segmented text

    Returns:
        str: clean segmented text
    """
    clean_segmented_text = segmented_text.replace('\n ', '\n')
    clean_segmented_text = clean_segmented_text.replace('  ', ' ')
    return clean_segmented_text


def post_process_human_data(human_data):
    """Remove unwanted space and solves double shad(ཉིས་ཤད་) split cases

    Args:
        human_data (str): human segmented data

    Returns:
        str: clean human segmented data
    """
    human_data = human_data.replace('།  །', '།།')
    human_data = human_data.replace('  ', ' ')
    return human_data

def get_toks(seg_str):
    """Extract list of tokens from segmented string

    Args:
        seg_str (str): segmented string which can be by human or botok

    Returns:
        list: list of tokens
    """
    tokens = [token for token in seg_str.split(' ') if token]
    return tokens

def parse_tok(botok_tok):
    """parse botok parts

    Args:
        botok_tok (str): botok tok

    Returns:
        str,str: text of token and pos of token
    """
    pos = re.search(r'<.*?>', botok_tok)[0]
    text = botok_tok.replace(pos, '')
    return text, pos

def get_bilou_tag_line(human_toks, botok_toks):
    """Add bilou tags to botok tokens and join them as a string with space between each tokens

    Args:
        human_toks (list): tokens from human segmented line
        botok_toks (list): tokens from botok segmented line

    Returns:
        str: botok tokens with bilou tag separated by space
    """
    bilou_tag_line = ''
    while True:
        human_tok = human_toks[0]
        cur_tok = ''
        tok_walker= 0
        while tok_walker < len(botok_toks):
            botok_tok_text, botok_tok_pos = parse_tok(botok_toks[tok_walker])
            if botok_tok_text == human_tok:
                bilou_tag_line += f'{botok_tok_text}{botok_tok_pos}/U '
                botok_toks = botok_toks[tok_walker+1:]
                break
            elif botok_tok_text in human_tok:
                cur_tok += botok_tok_text
                if cur_tok == human_tok:
                    bilou_tag_line += f'{botok_tok_text}{botok_tok_pos}/I '
                    botok_toks = botok_toks[tok_walker+1:]
                    break
                elif re.search(f'^{botok_tok_text}', human_tok):
                    bilou_tag_line += f'{botok_tok_text}{botok_tok_pos}/B '
                else:
                    bilou_tag_line += f'{botok_tok_text}{botok_tok_pos}/I '
            elif re.search(human_tok, botok_tok_text):
                cur_tok = human_tok
                bilou_tag_line += f'{botok_tok_text}{botok_tok_pos}/S '
                while re.search(cur_tok, botok_tok_text):
                    human_toks = human_toks[1:]
                    human_tok = human_toks[0]
                    cur_tok += human_tok
            else:
                botok_toks = botok_toks[tok_walker:]
                if tok_walker != 0:
                    break
                else:
                    bilou_tag_line += f'{botok_tok_text}{botok_tok_pos}/S '
            tok_walker += 1
        human_toks = human_toks[1:]
        if not human_toks:
            break
    return bilou_tag_line

def get_bilou_tag_data(corpus_data, human_data):
    """Corpus data get segmented by botok.
    Bilou tag is given to botok segmented data by comparing with human segmentation

    Args:
        corpus_data (str): corpus data (unsegmented data)
        human_data (str): segmented corpus data by human

    Returns:
        str: botok segmented data with bilou tag
    """
    botok_data = get_botok_segmentation(corpus_data)
    human_lines = human_data.splitlines()
    botok_lines = botok_data.splitlines()
    bilou_tag_data = ''
    for human_line, botok_line in zip(human_lines, botok_lines):
        human_toks = get_toks(human_line)
        botok_toks = get_toks(botok_line)
        bilou_tag_data += get_bilou_tag_line(human_toks, botok_toks) + '\n'
    return bilou_tag_data

def get_split_suggestions(bilou_tag_data):
    """Return all the tokens with Split tag(S)

    Args:
        bilou_tag_data (str): Botok segmented data with bilou tag

    Returns:
        list: list of tokens with split tags
    """
    split_suggestions = [split_token[:-2] for split_token in re.findall(r'\S+/S', bilou_tag_data)]
    return list(set(split_suggestions))

def get_merge_suggestions(bilou_tag_data):
    """Return all the tokens which are meant to be merge

    Args:
        bilou_tag_data (str): Botok segmented data with bilou tag

    Returns:
        list: list of tokens that are meant to be merge
    """
    merge_suggestions = [merge_suggestion for merge_suggestion,_ in re.findall(r'(\S+/B (\S+/I )+)', bilou_tag_data)]
    return list(set(merge_suggestions))

def parse_merge_suggestion(merge_suggestion):
    """Return tokens in merge suggestion

    Args:
        merge_suggestion (str): merge suggestion extracted from bilou tagged text

    Returns:
        list: tokens in merge suggestion
    """
    merge_suggestion_tokens = [re.search(r'(\S+)<\S+',token).group(1) for token in merge_suggestion.split(' ') if token]
    return merge_suggestion_tokens

def get_counter_merge_suggestion(merge_suggestion_tokens):
    """Return opposite of merge suggestion

    Args:
        merge_suggestion_tokens (list): tokens in merge suggestion

    Returns:
        str: opposite of merge suggestion
    """
    counter_merge_suggestion = ' '.join(merge_suggestion_tokens)
    if merge_suggestion_tokens[-1][-1] == '་':
        counter_merge_suggestion += " "
    return counter_merge_suggestion

def get_remove_word_candidates(split_suggestions, human_data):
    """Return remove word candidate or non ambiguous spilt options from spilt suggestions using human data

    Args:
        split_suggestions (list): spilt suggestion extracted from bilou tagged text
        human_data (str): human segmented text

    Returns:
        list: remove word candidates
    """
    remove_word_candidate = []
    for split_suggestion_token in split_suggestions:
        split_suggestion_tok_text = re.search(r'(\S+)<\S+',split_suggestion_token).group(1)
        if not is_single_syl(split_suggestion_tok_text):
            split_suggestion = f' {split_suggestion_tok_text} '
            splited_token, split_idx = splited_token_in_human_data(split_suggestion_tok_text, human_data)
            if split_suggestion not in human_data and splited_token:
                remove_word_candidate.append(split_suggestion_tok_text)
    return remove_word_candidate

def get_new_word_candidate(merge_suggestion, human_data):
    """Return new word if merge suggestion is not ambiguous one else empty string return

    Args:
        merge_suggestion (str): merge sugeestion
        human_data (str): human segmented data

    Returns:
        str: new word candidate
    """
    new_word = ''
    merge_suggestion_tokens = parse_merge_suggestion(merge_suggestion)
    new_word =  ''.join(merge_suggestion_tokens)
    # counter_merge_suggestion = " " + get_counter_merge_suggestion(merge_suggestion_tokens)
    splited_token, split_idx = splited_token_in_human_data(new_word, human_data)
    if not splited_token:
        return new_word
    else:
        return ''

def get_new_word_candidates(merge_suggestions, human_data):
    """Return all the new word candidate from merge suggestions using human data

    Args:
        merge_suggestions (list): merge suggestions extracted from bilou tagged text
        human_data (str): human segmented data

    Returns:
        list: new word candidate
    """
    new_word_candidate = []
    for merge_suggestion in merge_suggestions:
        new_word = get_new_word_candidate(merge_suggestion, human_data)
        if new_word:
            new_word_candidate.append(new_word)     
    return new_word_candidate

def filter_seg_errors(bilou_tag_data, human_data):
    """Filters out obivious segmentation error and extract new words and new remove words

    Args:
        bilou_tag_data (str): segmented botok data with bilou tag
        human_data (ste): segmented human data

    Returns:
        list: new word list and new remove word list
    """
    new_word_candidate = []
    new_remove_word_candidate = []
    split_suggestions = get_split_suggestions(bilou_tag_data)
    merge_suggestions = get_merge_suggestions(bilou_tag_data)
    new_word_candidate = get_new_word_candidates(merge_suggestions, human_data)  
    new_remove_word_candidate = get_remove_word_candidates(split_suggestions, human_data)
    return new_word_candidate, new_remove_word_candidate

def rdr_postprocess(file_path):
    suffixes = [".DICT", ".INIT", ".RAW", ".sDict"]
    for s in suffixes:
        Path(file_path.parent / (file_path.name + s)).unlink()

def remove_duplicate_word(word_list):
    return list(set(word_list))

def add_word_2_adjustment(words_2_add, corpus_file_name, dialect_pack_name, type='words'):
    """New word candidates or new remove word candidates are added with existing word list.
    Duplicates are then removed.
    Unique word list are then added to its file.

    Args:
        words_2_add (list): word list of new word candidates or new remove word candidates
        corpus_file_name (str): courpus file name
        dialect_pack_name (str): current working dialect pack name
        type (str, optional): type can be either words or remove. Defaults to 'words'.
    
    Returns:
        list: latest word list of mentioned type
    """
    old_word_list = []
    word_list_path = (DIALECT_PACK_DIR / dialect_pack_name / "adjustments" / type / f'{corpus_file_name}.tsv')
    if word_list_path.is_file():
        old_word_list = [old_word for old_word in word_list_path.read_text(encoding='utf-8-sig').splitlines() if old_word]
    new_word_list = old_word_list + words_2_add
    new_word_list = remove_duplicate_word(new_word_list)
    new_words = '\n'.join(new_word_list)
    word_list_path.write_text(new_words, encoding='utf-8-sig')
    print(f'[INFO]: New {type} added to adjustment {type} list..')
    return new_word_list

def get_bilou_rules(bilou_tag_data_path):
    """Extract rdr rules by training RDR model using bilou tagged data.
    Convert rdr rules to cql rules and returning it.

    Args:
        bilou_tag_data_path (pathlib): path of bilou tagged data

    Returns:
        list: rdr rules converted into cql rules 
    """
    log = r(str(bilou_tag_data_path), mode="train", verbose=True)
    print('[INFO]: RDR TRAINING COMPLETED..')
    rdr_rules = Path(f"{bilou_tag_data_path}.RDR").read_text(
        encoding="utf-8-sig"
    )
    bilou_rules = rdr_2_replace_matcher(rdr_rules).splitlines()
    bilou_rules = list(set(bilou_rules))
    return bilou_rules

def convert_bilou_rules(bilou_rules, bilou_tag_init, human_data):
    """Convert bilou rules to normal cql rules as rules with bilou tag are not usable by botok

    Args:
        bilou_rules (list): cql rules with bilou tag
        bilou_tag_init (str): bilou tagged initial text
        human_data (str): human segmented data

    Returns:
        list: usable cql rule by botok
    """
    new_cql_rules = []
    for bilou_rule in bilou_rules:
        tokens_info, index_info, operator, conclusion = parse_rule(bilou_rule)
        tokens_in_rule = get_tokens(tokens_info)
        ambiguous_seg_candidates = get_ambiguous_seg_candidates(tokens_in_rule, index_info, bilou_tag_init)
        new_cql_rules += get_new_rule(ambiguous_seg_candidates, int(index_info)+1, conclusion, human_data) # index incremented as extra context token involve
    new_cql_rules = list(set(new_cql_rules))
    return new_cql_rules

def extract_seg_rule(corpus_file_path, dialect_pack_name=DEFAULT_DPACK, type='cql', no_epochs = 3):
    """Extracts segmentation rules.

    Args:
        corpus_file_path (pathlib): input file's path
        dialect_pack_name (string, optional): name of dialect pack for which rules are. Defaults to DEFAULT_DPACK.
        type (str, optional): type of rules can be human friendly rule(hfr) or corpus query rule. Defaults to 'cql'.
        no_epochs (int, optional): Number of times word filters need to perform. Defaults to 3.

    Returns:
        str: segmentation rules
    """
    new_word_list = []
    new_remove_word_list = []
    corpus_file_name = corpus_file_path.stem
    number_of_segmentation = 1
    human_data = (corpus_file_path.parent / f'{corpus_file_name}_hd.txt').read_text(encoding='utf-8-sig')
    human_data = post_process_human_data(human_data)
    corpus_data = corpus_file_path.read_text(encoding='utf-8-sig')
    while True:
        bilou_tag_data = get_bilou_tag_data(corpus_data, human_data)
        print(f'[INFO]: SEGMENTATION PHASE {number_of_segmentation} COMPLETED..')
        new_word_list, new_remove_word_list = filter_seg_errors(bilou_tag_data, human_data)
        print('[INFO]: FILTER SEGMENTATION ERROR COMPLETED..')
        if new_word_list:
            new_word_list = add_word_2_adjustment(new_word_list, corpus_file_name, dialect_pack_name, type='words')
        if new_remove_word_list:
            new_remove_word_list = add_word_2_adjustment(new_remove_word_list, corpus_file_name, dialect_pack_name, type='remove')
        bilou_tag_data = get_bilou_tag_data(corpus_data, human_data)
        word_list, remove_word_list = filter_seg_errors(bilou_tag_data, human_data)
        new_remove_word_list = [remove_word for remove_word in remove_word_list if remove_word not in new_remove_word_list]
        new_word_list = [word for word in word_list if word not in new_word_list]
        number_of_segmentation += 1
        if (not new_word_list and not new_remove_word_list) or number_of_segmentation > no_epochs:
            break
    bilou_tag_data_path = (corpus_file_path.parent / f'{corpus_file_name}_tr_data.txt')
    bilou_tag_data_path.write_text(bilou_tag_data, encoding='utf-8')
    bilou_rules = get_bilou_rules(bilou_tag_data_path)
    (corpus_file_path.parent / f'{corpus_file_name}_bilou_rules.txt').write_text("\n".join(bilou_rules), encoding='utf-8')
    new_cql_rules = []
    bilou_tag_init = (corpus_file_path.parent / f'{bilou_tag_data_path.name}.INIT').read_text(encoding='utf-8-sig')
    new_cql_rules = convert_bilou_rules(bilou_rules, bilou_tag_init, human_data)
    new_cql_rules = "\n".join(new_cql_rules)
    rdr_postprocess(bilou_tag_data_path)
    if type != 'cql':
        new_cql_rules = cqlr2hfr(new_cql_rules)
    return new_cql_rules