import re

def get_syls(token):
    syls = []
    token_parts = re.split("(་)", token)
    syl = ''
    for walker, part in enumerate(token_parts):
        if part:
            if walker % 2 == 0:
                syl += part
            else:
                syl += part
                syls.append(syl)
                syl = ""
    return syls

def parse_rule(rule):
    """Parse all the components of cql rule

    Args:
        rule (str): cql rule

    Returns:
        str: token info, index info, operator of the rule and conclusion tag
    """
    part_of_rules = rule.split('\t')
    return part_of_rules[0], part_of_rules[1], part_of_rules[2], part_of_rules[3]

def get_tokens(tokens_info):
    """Parse tokens from tokens info of a cql rule

    Args:
        tokens_info (str): tokens info in a cql rule

    Returns:
        list: tokens from token info
    """
    tokens = re.findall(r'\[.*?\]', tokens_info)
    return tokens

def parse_tok(token):
    try:
        bilou_tag = re.search(r'pos="(\S)"', token).group(1)
    except:
        bilou_tag = ''
    try:
        text = re.search(r'text="(\S+)" ?', token).group(1)
    except:
        text = ''
    text = re.sub('\.', '\\\S', text)
    return bilou_tag, text

def add_extra_token_pat(ambiguous_seg_pat):
    """extra context tokens added to ambiguous seg pat

    Args:
        ambiguous_seg_pat (str): ambiguous segmentation pattern

    Returns:
        str: ambiguous seg pat with extra context token
    """
    extra_token_pat = r' \S+?/\S '
    ambiguous_seg_pat_with_extra_token_pat = f'{extra_token_pat}{ambiguous_seg_pat}{extra_token_pat}'
    ambiguous_seg_pat_with_extra_token_pat = ambiguous_seg_pat_with_extra_token_pat.replace('  ', ' ')
    return ambiguous_seg_pat_with_extra_token_pat

def get_ambiguous_seg_pat(tokens_in_rule, index_info):
    """Return ambguous segmentation's pattern

    Args:
        tokens_in_rule (list): tokens in bilou rule

    Returns:
        str: ambiguos segmentation's pattern
    """
    ambiguous_seg_pat = ''
    for token in tokens_in_rule:
        bilou_tag, text = parse_tok(token)
        if text:
            ambiguous_seg_pat += f' {text}'
            if bilou_tag:
                ambiguous_seg_pat += f'/{bilou_tag}'
            else:
                ambiguous_seg_pat += r'/\S'
        else:
            ambiguous_seg_pat += r" \S+?"
            if bilou_tag:
                ambiguous_seg_pat += f'/{bilou_tag}'
            else:
                ambiguous_seg_pat += r'/\S'
    if len(tokens_in_rule) < 4:
        ambiguous_seg_pat = add_extra_token_pat(ambiguous_seg_pat)
    return ambiguous_seg_pat

def construct_token_info(ambiguous_seg_candidate):
    """Construct token info part of a cql rule

    Args:
        ambiguous_seg_candidate (list): ambiguous segmentation candidate's token list

    Returns:
        str: token info part of a cql rule
    """
    token_info = ''
    for token in ambiguous_seg_candidate:
        token_parts = token.split('/')
        token_text = re.search(r'(\S+)<\S+',token_parts[0]).group(1)
        token_pos = re.search(r'<(\S+)>',token_parts[0]).group(1)
        if token_pos != 'NO_POS':
            token_info += f'[text="{token_text}" & pos="{token_pos}"] '
        else:
            token_info += f'[text="{token_text}"] '
    return token_info.strip()

def get_ambiguous_seg_candidates(tokens_in_rule, index_info, bilou_tag_data):
    """Return all the possible ambiguous segmentation candidates containing tokens in rule

    Args:
        tokens_in_rule (list): tokens in bilou rule
        bilou_tag_data (str): bilou tagged data

    Returns:
        list: ambiguous segmentation candidates
    """
    ambiguous_seg_candidates_tokens = []
    ambiguous_seg_pat = get_ambiguous_seg_pat(tokens_in_rule, index_info)
    ambiguous_seg_candidates = re.findall(ambiguous_seg_pat, bilou_tag_data)
    ambiguous_seg_candidates = list(set(ambiguous_seg_candidates))
    for ambiguous_seg_candidate in ambiguous_seg_candidates:
        ambiguous_seg_candidates_tokens.append([token for token in ambiguous_seg_candidate.split(' ') if token])
    return ambiguous_seg_candidates_tokens

def is_single_syl(token):
    """Check token is single syllable

    Args:
        token (str): token

    Returns:
        boolean: True if token is single syllable else False
    """
    syls = [syl for syl in token.split('་') if syl]
    if len(syls) > 1:
        return False
    else:
        return True

def parse_index_info(index_info):
    """Return index of the token from index info

    Args:
        index_info (str): index info of a cql rule

    Returns:
        int: index of token
    """
    if '-' in index_info:
        index_info_parts = index_info.split('-')
        index = int(index_info_parts[0])
    else:
        index = int(index_info)
    return index

def splited_token_in_human_data(split_tok_text, human_data):
    spilt_suggestion = split_tok_text.strip()
    syls = get_syls(spilt_suggestion)
    for syl_walker, syl in enumerate(syls):
        split_possible = f' {syl} {"".join(syls[syl_walker+1:])} '
        if split_possible in human_data:
            return split_possible, syl_walker+1
    return '', 0

def get_splited_token(spilt_suggestion):
    """Split split suggestion and return it

    Args:
        spilt_suggestion (str): split suggestion

    Returns:
        str: opposite of split suggestion
    """
    spilt_suggestion = spilt_suggestion.strip()
    syls = [syl.strip() for syl in spilt_suggestion.split('་') if syl and syl != ' ']
    suggestion = f'{syls[0]}་ {"་".join(syls[1:])}'
    if spilt_suggestion[-1] == '་':
        suggestion += '་'
    splited_token = f' {suggestion} '
    return splited_token

def is_false_positive_split(tokens_in_rule, index, splited_token, human_data):
    """Check if the rule is a false positive split case or not

    Args:
        tokens_in_rule (list): tokens in rule
        index (int): index of token on which split is going to take
        splited_token (str): splited token
        human_data (str): human segmented data

    Returns:
        boolean: True if rule is false positive else false
    """
    split_suggestion_with_context = ''
    splited_token = splited_token.strip()
    for token_walker, token in enumerate(tokens_in_rule, 1):
        token_text = re.search(r'text=\"(\S+)\"', token).group(1)
        if token_walker == 1:
            split_suggestion_with_context += f' {token_text} '
        elif token_walker == index:
            split_suggestion_with_context += f'{splited_token} '
        else:
            split_suggestion_with_context += f'{token_text} '
    if split_suggestion_with_context in human_data:
        return False
    else:
        return True

def is_invalid_split(tokens_info, index_info, human_data):
    """Return false if split suggestion is ambiguous segmentation else true 

    Args:
        tokens_info (str): token info of a rule
        index_info (str): index info of a cql rule
        human_data (str): human segmented data

    Returns:
        boolean: True if invalid split rule else False
    """
    index = parse_index_info(index_info)
    tokens = get_tokens(tokens_info)
    token_to_split = re.search(r'text=\"(\S+)\"', tokens[index-1]).group(1)
    if is_single_syl(token_to_split) or len(tokens) < index:
        return True, 0
    else:
        split_suggestion = f" {token_to_split} "
        splited_token, split_idx = splited_token_in_human_data(split_suggestion, human_data)
        if split_suggestion in human_data and splited_token and not is_false_positive_split(tokens, index, splited_token, human_data):
            return False, split_idx
        else:
            return True, 0

def is_false_positive_merge(tokens_in_rule, index, human_data):
    """Check if rule is false positive merge or not

    Args:
        tokens_in_rule (list): tokens in rule
        index (int): index of token on which merge operation is going to perform
        human_data (str): human segmented data

    Returns:
        boolean: true if rule is false positive merge else false
    """
    merge_suggestion_with_context = ''
    for token_walker, token in enumerate(tokens_in_rule, 1):
        token_text = re.search(r'text=\"(\S+)\"', token).group(1)
        if token_walker == 1:
            merge_suggestion_with_context += f' {token_text} '
        elif token_walker == index:
            merge_suggestion_with_context += f'{token_text}'
        elif token_walker == index+1:
            merge_suggestion_with_context += f'{token_text} '
        else:
            merge_suggestion_with_context += f'{token_text} '
    if merge_suggestion_with_context in human_data:
        return False
    else:
        return True

def is_invalid_merge(tokens_info, index_info, human_data):
    """Return false if merge suggestion is ambiguous segmentation else true 

    Args:
        tokens_info (str): token info of a rule
        index_info (str): index info of a cql rule
        human_data (str): human segmented data

    Returns:
        boolean: True if invalid merge rule else False
    """
    index = parse_index_info(index_info)
    tokens = get_tokens(tokens_info)
    if len(tokens) <= index or index == 0:
        return True
    else:
        part1 = re.search(r'text=\"(\S+)\"', tokens[index-1]).group(1)
        part2 = re.search(r'text=\"(\S+)\"', tokens[index]).group(1)
        merge_suggestion = f' {part1}{part2} '
        splited_token_in_hd, split_idx = splited_token_in_human_data(merge_suggestion, human_data)
        if "།" not in merge_suggestion and (merge_suggestion in human_data and splited_token_in_hd) and not is_false_positive_merge(tokens, index, human_data):
            return False
        else:
            return True

def filter_valid_rules(new_rules, human_data):
    """Return valid rules which can solve ambiguous segmentation errors

    Args:
        new_rules (list): cql rules
        human_data (str): human segmented data

    Returns:
        list: cql rules
    """
    valid_rules = []
    for new_rule in new_rules:
        tokens_info, index_info, operator, conclusion = parse_rule(new_rule)
        if ":" == operator:
            is_invalid_split_flag, split_idx = is_invalid_split(tokens_info, index_info, human_data)
            if not is_invalid_split_flag:
                new_rule = re.sub(r'-\d', f'-{split_idx}', new_rule)
                valid_rules.append(new_rule)
        elif "+" == operator:
            if not is_invalid_merge(tokens_info, index_info, human_data):
                valid_rules.append(new_rule)
    return valid_rules

def get_new_rule(ambiguous_seg_candidates, index, conclusion, human_data):
    """Return list of usable cql rules by botok

    Args:
        ambiguous_seg_candidates (list): ambiguous segmentation candidates
        index (int): index of token on which operation needs to perform
        conclusion (str): conclusion tag of rule
        human_data (str): human segmented data

    Returns:
        list: usable cql rules of botok
    """
    new_rules = []
    for ambiguous_seg_candidate in ambiguous_seg_candidates:
        new_rule = f"{construct_token_info(ambiguous_seg_candidate)}\t"
        if 'B' in conclusion:
            new_rule += f'{index}\t+\t[]'
        elif 'I' in conclusion:
            new_rule += f'{index-1}\t+\t[]'
        elif 'S' in conclusion:
            new_rule += f'{index}-1\t:\t[] []'
        else:
            new_rule = ''
        if new_rule:
            new_rules.append(new_rule)
    unique_rules = list(set(new_rules))
    filtered_rules = filter_valid_rules(unique_rules, human_data)
    return filtered_rules