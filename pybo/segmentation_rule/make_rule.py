import re

def parse_rule(rule):
    part_of_rules = rule.split('\t')
    return part_of_rules[0], int(part_of_rules[1]), part_of_rules[2], part_of_rules[3]

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
    token_pat = get_token_pat(tokens)
    # todo: Selecting only one possibility.. need to find all possibilities and select the abiguious one
    try:
        token_in_training = re.search(token_pat, training_data)[0]
    except:
        print(f'{token_pat} pattern not found')
        token_in_training = ''
    tokens_of_interest = [token for token in token_in_training.split(' ') if token]
    return tokens_of_interest

def get_new_rule(tokens_of_interest, index, conclusion):
    new_rule = f"{construct_token_of_rule(tokens_of_interest)}\t"
    if 'B' in conclusion:
        new_rule += f'{index}\t+\t[]'
    elif 'I' in conclusion:
        new_rule += f'{index-1}\t+\t[]'
    elif 'S' in conclusion:
        new_rule += f'{index}-1\t:\t[] []'
    else:
        new_rule += f'{index}\t=\t[]'
    return new_rule

def convert_split_ambiguity_2_rule(ambiguity):
    tokens_of_interest = [token for token in ambiguity.split(' ') if token]
    rule = get_new_rule(tokens_of_interest, 2, 'S')
    return rule

def get_split_rules(training_init):
    split_rules = []
    split_ambiguities = re.findall('\S+/\S \S+?/S \S+?/\S', training_init)
    for split_ambiguity in split_ambiguities:
        split_rules.append(convert_split_ambiguity_2_rule(split_ambiguity))
    return list(set(split_rules))