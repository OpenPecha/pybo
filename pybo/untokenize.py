
def pre_processing(tokenized_text):
    tokens = [token for token in tokenized_text.split(' ') if token]
    return tokens

def get_token_text(token):
    token_parts = [part for part in token.split('/') if part]
    return token_parts[0]

def assemble(tokens):
    detokenized_text = ''
    for token in tokens:
        detokenized_text += get_token_text(token)
    return detokenized_text
