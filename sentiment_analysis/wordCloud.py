import nltk
from nltk.tokenize import word_tokenize
import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
import string
from wordcloud import WordCloud
from nltk import sent_tokenize, word_tokenize
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import matplotlib
nltk.download("stopwords")

news = pd.read_csv("fake.csv")
# print(news['title'])
a = news['title'].str.lower().str.cat(sep=' ')
b = re.sub('[^A-Za-z]+', ' ', a)
# print(str(b))
 
def preprocess():
	stop_words  = stopwords.words('english')  
	word_tokens = word_tokenize(b) 
	cleanwords = [i for i in word_tokens if i not in stop_words and i.isalpha() and len(i) > 2]

	wc(cleanwords)
    # if lowercase:
    #     word_tokens = [token if emoticon_re.search(token) else token.lower() for token in word_tokens]
    # return word_tokens

def wc(cleanwords):
    wordcloud2 = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=1200,
                          height=1000
                         ).generate(" ".join(cleanwords))
    plt.imshow(wordcloud2)
    plt.axis('off')
    plt.show()
 
if __name__ == "__main__":
	preprocess()