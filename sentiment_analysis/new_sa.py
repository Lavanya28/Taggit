import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from textblob import TextBlob
import re
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import nltk
import seaborn as sns
import sys
reload(sys)
sys.setdefaultencoding('utf8')
nltk.download("stopwords")


matplotlib.style.use('ggplot')
news = pd.read_csv("fake.csv")

def get_tweets():
	text_list = news['text'].tolist()
	# print(text_list)

	tweet_sentiment_list = []

	# count = 0
	for tweet in text_list:
		mini_dict = {}
		mini_dict['text'] = tweet
		mini_dict['sentiment'] = get_tweet_sentiment(clean_tweet(tweet))
		tweet_sentiment_list.append(mini_dict)
		# print(get_tweet_sentiment(clean_tweet(tweet)))

		# if count == 3:
			# break

		# count = count + 1
		
	return tweet_sentiment_list

def pos_vs_neg():
	tweet_sentiment_list = get_tweets()
	# print(tweet_sentiment_list)
	
	pos = []
	neg = []
	for dct in tweet_sentiment_list: 
		if dct['sentiment'] == 'positive':
			pos.append(dct['text'].lower())

		if dct['sentiment'] == 'negative':
			neg.append(dct['text'].lower())
    
	# print(str(pos))
	print(str(neg))
	# graph(pos)
	graph(neg)

def graph(sentiment_list):
	stop_words  = stopwords.words('english')  
	word_tokens = []
	
	for text in sentiment_list:
		tokens = word_tokenize(text.decode('utf-8').strip())
		# print(tokens)
		for word in tokens:
			word_tokens.append(word)


	cleanwords = [i for i in word_tokens if i not in stop_words and i.isalpha() and len(i) > 2]

	word_dist = nltk.FreqDist(cleanwords)
	rslt = pd.DataFrame(word_dist.most_common(100),
	            columns=['Word', 'Frequency'])

	plt.figure(figsize=(5,5))
	sns.set_style("whitegrid")
	ax = sns.barplot(x="Word",y="Frequency", data=rslt.head(7))
	plt.show()

def clean_tweet(tweet):

	emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

	regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
	]

	tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
	# remove = re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet)
	# join_words = ' '.join(remove.split())
	test = tokens_re.findall(str(tweet))
	s = ' '.join(test)
	return s.decode('latin-1').encode("utf-8")
    # return join_words
 
def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)

    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
		
if __name__ == "__main__":
	pos_vs_neg()
