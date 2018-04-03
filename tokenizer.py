'''
    Tokenizer for the tweets. We're not using NLTK tokenizer here because it tokenizes :D as [':', 'D'], same for hashtags etc.
'''

import re # regular expression lib
import json
from nltk.tokenize import TweetTokenizer

# https://stackoverflow.com/questions/14571103/capturing-emoticons-using-regular-expression-in-python - regex for emoticons
emoticons = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

# https://sites.google.com/site/miningtwitter/questions/user-tweets/contain-hashtags
regex = [
    emoticons,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

compiled_regex, compiled_emoticons = re.compile(r'('+'|'.join(regex) +')', re.VERBOSE | re.IGNORECASE), re.compile(r'^'+ emoticons +'$', re.VERBOSE | re.IGNORECASE)

'''
    Tokenizer based on the compiled regex.
'''
def tokenize(str):
    return compiled_regex.findall(str)

def tokenize_with_casing(str, lowercase=False):
    tokens = tokenize(str)
    if lowercase:
        new_tokens = []
        for token in tokens:
            if compiled_emoticons.search(token):
                new_tokens.append(token)
            else:
                new_tokens.append(token.lower())
        return new_tokens
    return tokens

'''
    Tokenize our data.
    NOTE: set @param withLibrary: tokenize with library TweetTokenizer from NLTK
'''
def tokenize_corpus(filename='data.json', lowercase=False, withLibrary=False):
    tokenized_array = []
    with open(filename, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            tokens = []
            if withLibrary:
                tknzr = TweetTokenizer(preserve_case= not lowercase)
                tokens = tknzr.tokenize(tweet['text'])
            else:
                tokens = tokenize_with_casing(tweet['text'], lowercase)
            tokenized_array.append(tokens)
    return tokenized_array

# print(tokenize_corpus())
