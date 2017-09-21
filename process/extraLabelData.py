#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.feature_extraction.text import CountVectorizer 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import TfidfTransformer 
import os
import nltk

txt_arr = []
txt_label = []


txt_content=open(r'citation_sentiment_corpus.txt','r')
txt=txt_content.read()
txt.decode('utf-8')
strs = txt.split('\n')

for temp in strs:
	temps = temp.split('\t');
	txt_label.append(temps[2]);
	txt_arr.append(temps[3]);

english_punctuations = [',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%']

vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=4, max_df=10, stop_words=english_punctuations) 
tfidf_train = vectorizer.fit_transform(txt_arr)
print "the shape of train is "+repr(tfidf_train.shape)  

result = tfidf_train.toarray()

output = open('outputExtraData.txt','w')
for i in range(0, len(result)):
	if txt_label[i] == 'p':
		output.write('1'+' ')
	elif txt_label[i] == 'n':
		output.write('-1'+' ')
	else:
		output.write('0'+' ')
	for j in range(0, len(result[i])):
		if result[i][j] != 0:
			output.write(str(j)+':'+str(result[i][j])+" ")
	output.write('\n')