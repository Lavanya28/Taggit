'''
    Removing stop words from the corpus.
'''
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk import ngrams
from tokenizer import tokenize_corpus

stop_words = list(string.punctuation) + list(stopwords.words('english')) + ['rt', '…', '’'] + ['#trump', '#election', '#hillary']
# add the original hashtags as well, TODO: change this later to accept paramters of query hashtags

'''
    Simple method to strip all stop words from corpus.
    NOTE: @param corpus is a 2D array (list[list])
'''
def remove_stop_words_from_corpus(corpus):
    ret = []
    for tweet in corpus:
        ret.append(remove_stop_words_from_line(tweet))
    return ret

'''
    Simple method to remove all stop words from a single line of text.
'''
def remove_stop_words_from_line(tweet):
    return [word for word in tweet if word not in stop_words]

'''
    Simple method to count term occurences in ALL of corpus data. (TODO: modify to do per tweet/line)
    NOTE: parameters preceed each other. Meaning, if @onlyHashtags is set,
          all other parameter values will be disregarded whether they are set or not.
'''
def count_occurences(onlyHashtags=False, onlyMentions=False, noTweetJargon=False, bigram=False, trigram=False):
    count = Counter()
    bag = tokenize_corpus(lowercase=True, withLibrary=False)
    for line in bag:
        line_fresh = remove_stop_words_from_line(line)
        hashtags = [word for word in line_fresh if word.startswith('#')]
        mentions = [word for word in line_fresh if word.startswith('@')]
        no_jargon = [word for word in line_fresh if word not in stop_words and not word.startswith(('#', '@'))]
        line_bigram = ngrams(no_jargon, 2) # change this to either of the above to generate different bigrams
        line_trigram = ngrams(no_jargon, 3)
        if onlyHashtags:
            count.update(hashtags)
        elif onlyMentions:
            count.update(mentions)
        elif noTweetJargon:
            count.update(no_jargon)
        elif bigram:
            count.update(line_bigram)
        elif trigram:
            count.update(line_trigram)
        else:
            count.update(line_fresh)
    print(count.most_common(10))

# count_occurences(trigram=True)
