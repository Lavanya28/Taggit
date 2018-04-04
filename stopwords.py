'''
    Removing stop words from the corpus.
'''
import string
from nltk.corpus import stopwords
from collections import Counter, defaultdict
from nltk import ngrams
from tokenizer import tokenize_corpus
import operator

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
def count_occurences(onlyHashtags=False, onlyMentions=False, noTweetJargon=False, ngram=[False, 0], n=10):
    count = Counter()
    bag = tokenize_corpus(lowercase=True, withLibrary=False)
    for line in bag:
        line_fresh = remove_stop_words_from_line(line)
        hashtags = [word for word in line_fresh if word.startswith('#')]
        mentions = [word for word in line_fresh if word.startswith('@')]
        no_jargon = [word for word in line_fresh if word not in stop_words and not word.startswith(('#', '@'))]
        if onlyHashtags:
            count.update(hashtags)
        elif onlyMentions:
            count.update(mentions)
        elif noTweetJargon:
            count.update(no_jargon)
        elif ngram[0]:
            line_ngram = ngrams(no_jargon, ngram[1]) # change this to either of the above to generate different bigrams
            count.update(line_ngram)
        else:
            count.update(line_fresh)
    return count.most_common(n)

# print(count_occurences(trigram=True))

'''
    Count term co-occurences.
'''
def term_cooccurences(n=10):
    count = defaultdict(lambda : defaultdict(int))
    bag = tokenize_corpus(lowercase=True, withLibrary=False)

    for line in bag:
        no_tweet_jargon = [term for term in line
                  if term not in stop_words
                  and not term.startswith(('#', '@'))]

        # Build co-occurrence matrix
        for i in range(len(no_tweet_jargon)-1):
            for j in range(i+1, len(no_tweet_jargon)):
                word1, word2 = sorted([no_tweet_jargon[i], no_tweet_jargon[j]])
                if word1 != word2:
                    count[word1][word2] += 1

    tuples = []
    # sort the defaultdict
    for k in count:
        sorted_count = sorted(count[k].items(), key=operator.itemgetter(1), reverse=True)
        for k1, v in sorted_count:
            tuples.append(((k, k1), v))

    #sort tuples by value
    sorted_tuples = sorted(tuples, key=operator.itemgetter(1), reverse=True)

    return sorted_tuples[:n]

# print(term_cooccurences(n=20))
