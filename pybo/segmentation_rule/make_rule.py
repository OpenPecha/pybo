import re

def parse_rule(rule):
    part_of_rules = rule.split('\t')
    return part_of_rules[0], part_of_rules[1], part_of_rules[2], part_of_rules[3]

def get_tokens(tokens_info):
    tokens = re.findall('\[.*?\]', tokens_info)
    return tokens

def parse_tok(tokens):
    try:
        pos = re.search('pos="(\S)"', tokens).group(1)
    except:
        pos = ''
    try:
        text = re.search('text="(\S+)" ?', tokens).group(1)
    except:
        text = ''
    return pos, text

def get_token_pat(tokens):
    result = ''
    for token in tokens:
        pos, text = parse_tok(token)
        if text:
            result += f' {text}'
            if pos:
                result += f'/{pos}'
            else:
                result += r'/\S'
        else:
            result += r" \S+?"
            if pos:
                result += f'/{pos}'
            else:
                result += r'/\S'
    return result

def construct_token_of_rule(tokens_of_interest):
    rule = ''
    for token in tokens_of_interest:
        token_parts = token.split('/')
        rule += f'["{token_parts[0].replace(" ", "")}"] '
    return rule.strip()

def get_match_tokens(tokens, training_data):
    tokens_of_interest = []
    token_pat = get_token_pat(tokens)
    tokens_in_training = re.findall(token_pat, training_data)
    tokens_in_training = list(set(tokens_in_training))
    for token_in_training in tokens_in_training:
        tokens_of_interest.append([token for token in token_in_training.split(' ') if token])
    return tokens_of_interest

def is_single_sly(token):
    text = re.search('\"(\S+)\"', token).group(1)
    syls = [syl for syl in text.split('་') if syl]
    if len(syls) > 1:
        return False
    else:
        return True

def parse_index_info(index_info):
    if '-' in index_info:
        index_info_parts = index_info.split('-')
        index = int(index_info_parts[0])
    else:
        index = int(index_info)
    return index

def is_invalid_split(tokens_info, index_info, human_data):
    index = parse_index_info(index_info)
    tokens = get_tokens(tokens_info)
    if is_single_sly(tokens[index-1]) or len(tokens) < index:
        return True
    else:
        split_suggestion = re.search('\"(\S+)\"', tokens[index-1]).group(1)
        if split_suggestion not in human_data:
            return True
        else:
            return False

def is_invalid_merge(tokens_info, index_info, human_data):
    index = parse_index_info(index_info)
    tokens = get_tokens(tokens_info)
    if len(tokens) <= index or index == 0:
        return True
    else:
        part1 = re.search('\"(\S+)\"', tokens[index-1]).group(1)
        part2 = re.search('\"(\S+)\"', tokens[index]).group(1)
        merge_suggestion = part1 + part2
        if "།" in merge_suggestion or merge_suggestion not in human_data:
            return True
        else:
            return False

def filter_invalid_rules(new_rules, human_data):
    valid_rules = []
    for new_rule in new_rules:
        if new_rule:
            tokens_info, index_info, operator, conclusion = parse_rule(new_rule)
            if ":" == operator:
                if not is_invalid_split(tokens_info, index_info, human_data):
                    valid_rules.append(new_rule)
            elif "+" == operator:
                if not is_invalid_merge(tokens_info, index_info, human_data):
                    valid_rules.append(new_rule)
    return valid_rules

def get_new_rule(tokens_of_interest, index, conclusion, human_data):
    new_rules = []
    for token_of_interest in tokens_of_interest:
        new_rule = f"{construct_token_of_rule(token_of_interest)}\t"
        if 'B' in conclusion:
            new_rule += f'{index}\t+\t[]'
        elif 'I' in conclusion:
            new_rule += f'{index-1}\t+\t[]'
        elif 'S' in conclusion:
            new_rule += f'{index}-1\t:\t[] []'
        else:
            new_rule = ''
        new_rules.append(new_rule)
    unique_rules = list(set(new_rules))
    filtered_rules = filter_invalid_rules(unique_rules, human_data)
    return filtered_rules