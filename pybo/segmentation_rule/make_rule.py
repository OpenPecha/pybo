import re

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
    return bilou_tag, text

def add_extra_token_pat(ambiguous_seg_pat, index_info):
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
    if len(tokens_in_rule) < 5:
        ambiguous_seg_pat = add_extra_token_pat(ambiguous_seg_pat, index_info)
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
        token_info += f'["{token_parts[0].replace(" ", "")}"] '
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

def get_counter_split_suggestion(spilt_suggestion):
    """Return opposite of split suggestion

    Args:
        spilt_suggestion (str): split suggestion

    Returns:
        str: opposite of split suggestion
    """
    syls = [syl.strip() for syl in spilt_suggestion.split('་') if syl and syl != ' ']
    suggestion = f'{syls[0]}་ {"་".join(syls[1:])}'
    if spilt_suggestion[-2] == '་':
        suggestion += '་'
    counter_split_suggestion = f' {suggestion} '
    return counter_split_suggestion

def is_false_positive_split(tokens_in_rule, index, counter_split_suggestion, human_data):
    """Check if the rule is a false positive split case or not

    Args:
        tokens_in_rule (list): tokens in rule
        index (int): index of token on which split is going to take
        counter_split_suggestion (str): co
        human_data (str): human segmented data

    Returns:
        boolean: True if rule is false positive else false
    """
    split_suggestion_with_context = ''
    counter_split_suggestion = counter_split_suggestion.strip()
    for token_walker, token in enumerate(tokens_in_rule, 1):
        token_text = re.search(r'\"(\S+)\"', token).group(1)
        if token_walker == 1:
            split_suggestion_with_context += f' {token_text} '
        elif token_walker == index:
            split_suggestion_with_context += f'{counter_split_suggestion} '
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
    token_to_split = re.search(r'\"(\S+)\"', tokens[index-1]).group(1)
    if is_single_syl(token_to_split) or len(tokens) < index:
        return True
    else:
        split_suggestion = f" {token_to_split} "
        counter_split_suggestion = get_counter_split_suggestion(split_suggestion)
        if split_suggestion in human_data and counter_split_suggestion in human_data and not is_false_positive_split(tokens, index, counter_split_suggestion, human_data):
            return False
        else:
            return True

def is_false_positive_merge(tokens_in_rule, index, human_data):
    merge_suggestion_with_context = ''
    for token_walker, token in enumerate(tokens_in_rule, 1):
        token_text = re.search(r'\"(\S+)\"', token).group(1)
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
        part1 = re.search(r'\"(\S+)\"', tokens[index-1]).group(1)
        part2 = re.search(r'\"(\S+)\"', tokens[index]).group(1)
        merge_suggestion = f' {part1}{part2} '
        counter_merge_suggestion = f' {part1} {part2} '
        if "།" not in merge_suggestion and (merge_suggestion in human_data and counter_merge_suggestion in human_data) and not is_false_positive_merge(tokens, index, human_data):
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
            if not is_invalid_split(tokens_info, index_info, human_data):
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