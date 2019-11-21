import re

cqlr = '''
[pos="DET" & སུ་] [pos="SCONJ"]	2	=	[pos="ADP"]
["སུ་"] [pos="PRON"] ["ནས་" & pos="SCONJ"]	3	=	[pos="SCONJ"]
'''

def splitToken(token):
    token = re.split(r' *& *', token)
    return token

def parseTokens(columns):
    tokens = []
    for line in columns:
        if len(line) == 4:
            # split tokens
            line[0] = re.findall(r'\[(.+?)\]', line[0])
            line[3] = re.findall(r'\[(.+?)\]', line[3])
            tokens.append(line)
            # split elements within tokens
            line[0] = [splitToken(token) for token in line[0]]
            line[3] = [splitToken(token) for token in line[3]]
        else:
            tokens.append(line)
    return tokens

def parseCql(string):
    # split lines
    lines = cqlr.splitlines()
    # split colums in lines
    columns = [line.split('\t') for line in lines]
    # split tokens in cql expressions
    tokens = parseTokens(columns)
    # split elements in tokens
    # elements = parseElements(tokens)
    return tokens

def translate2Hfr(tokens):
    parsedHfr = []
    # replace with regexes at token element level
    # element without = is the text
    return parsedHfr


def serializeHfr(tokens):
    hfr = []
    # merge lists
    return hfr

def cql2hfr(cqlr):
    parsedCqlr = parseCql(cqlr)
    parsedHfr = translate2Hfr(parsedCqlr)
    hfr = serializeHfr(parsedHfr)
    print(f'cqlr: {hfr}')



cql2hfr(cqlr)

    # return hfr


    


