import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist



def create_word_scores():
    posWords = pickle.load(open('D:/code/sentiment_test/pos_review.pkl','r'))
  .....
    return word_scores #包括了每个词和这个词的信息量


def bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)  #把文本变成双词搭配的形式
    bigrams = bigram_finder.nbest(score_fn, n) #使用了卡方统计的方法，选择排名前1000的双词
    return bag_of_words(bigrams)
def bag_of_words(words):
    return dict([(word, True) for word in words])
 def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)  #所有词和（信息量大的）双词搭配一起作为特征
def create_word_bigram_scores():
    posdata = pickle.load(open('D:/code/sentiment_test/pos_review.pkl','r'))
    negdata = pickle.load(open('D:/code/sentiment_test/neg_review.pkl','r'))
    return word_scores

 
