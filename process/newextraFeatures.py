#!/usr/bin/env python
# -*- coding: utf-8 -*-
print '*************************\n特征提取\n*************************'  
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.feature_extraction.text import CountVectorizer 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfTransformer 
import os
import nltk

listfile=os.listdir('/home/emily/Desktop/Data/')

txt_arr=[]

for i in range(0,2000):
    txt_content=open(r'/home/emily/Desktop/Data/'+listfile[i],'r')
    txt=txt_content.read()
    txt.decode('utf-8')
    txt_arr.append(txt)
    txt_content.close();

listfiletest=os.listdir('/home/emily/Desktop/TestData/')

test_arr=[]

for i in range(0,3000):
    test_content=open(r'/home/emily/Desktop/TestData/'+listfiletest[i],'r')
    test=test_content.read()
    test.decode('utf-8')
    test_arr.append(test)
    test_content.close();

# english_stopwords = stopwords.words('english')
# texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]

#去除标点符号
english_punctuations = [',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%']
# texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]


#按照单词和双词特征提取tf-idf，限制最小最大df
vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=4, stop_words=english_punctuations) 

tfidf_train = vectorizer.fit_transform(txt_arr)
wordlist = vectorizer.get_feature_names()#获取词袋模型中的所有词

tfidf_test = vectorizer.fit_transform(test_arr)
wordtestlist = vectorizer.get_feature_names()#获取词袋模型中的所有词test

print "the shape of train is "+repr(tfidf_train.shape)  
print "the shape of test is "+repr(tfidf_test.shape)  

result = tfidf_train.toarray()
resulttest = tfidf_test.toarray()

output = open('corpusBI/'+'data_train.svmlight','w')
for doc in result:
	output.write('0'+' ')
	for i in range(0, len(doc)):
		if doc[i] != 0:
			output.write(str(i)+':'+str(doc[i])+" ")
	output.write('\n')
outputtest = open('corpusBI/'+'data_test.svmlight','w')
for doc in resulttest:
	outputtest.write('0'+' ')
	for i in range(0, len(doc)):
		if doc[i] != 0:
			outputtest.write(str(i)+':'+str(doc[i])+" ")
	outputtest.write('\n')