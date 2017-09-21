#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer 
# corpus=['UNC played Duke in basketball','Duke lost the basketball game','I ate a sandwich']

# count_v1= CountVectorizer(stop_words = 'english', max_df = 0.5);
# counts_train =count_v1.fit_transform(corpus);

# print counts_train

# count_v2 = CountVectorizer(vocabulary=count_v1.vocabulary_);  
# counts_test = count_v2.fit_transform(corpus); 

# print counts_test

# tfidftransformer = TfidfTransformer();  
  
# tfidf_train = tfidftransformer.fit(counts_train).transform(counts_train);  
# tfidf_test = tfidftransformer.fit(counts_test).transform(counts_test); 

# print tfidf_train
print '*************************\nTfidfVectorizer\n*************************'  
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.feature_extraction.text import CountVectorizer 
import os
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

listfile=os.listdir('/home/emily/Desktop/Data')

txt_arr=[]

for i in range(9):
    txt_content=open(r'/home/emily/Desktop/Data/'+listfile[i],'r')
    txt=txt_content.read()
    txt.decode('utf-8')
    txt_arr.append(txt)
    txt_content.close();

#对文档单词进行小写化并进行分词
texts_tokenized = [[word.lower() for word in nltk.word_tokenize(document.decode('utf-8'))] for document in txt_arr]


#去除英文停用词
english_stopwords = stopwords.words('english')
texts_filtered_stopwords = [[word for word in document if not word in english_stopwords] for document in texts_tokenized]

#去除标点符号
english_punctuations = [',','.',':',';','?','(',')','[',']','&','!','*','@','#','$','%']
texts_filtered = [[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]


#中心词，词元化
wnl = nltk.WordNetLemmatizer()
texts_lemmatized=[[wnl.lemmatize(word) for word in document] for document in texts_filtered]


#去掉低频词
all_stems = sum(texts_lemmatized, [])
stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
texts = [[stem for stem in text if stem not in stems_once] for text in texts_lemmatized]

# tv = TfidfVectorizer(sublinear_tf = True, max_df = 1, stop_words = 'english');  
tv = CountVectorizer(stop_words = 'english', max_df = 0.5);
tfidf_train_2 = tv.fit_transform(txt_arr);  

tv2 = CountVectorizer(vocabulary = tv.vocabulary_);  
tfidf_test_2 = tv2.fit_transform(txt_arr);  
print "the shape of train is "+repr(tfidf_train_2.shape)  
print "the shape of test is "+repr(tfidf_test_2.shape)  
analyze = tv.build_analyzer()  
tv.get_feature_names()#statistical features/terms  

result = tfidf_train_2.toarray()
output = open(r'corpusBI/'+'data9_train.svmlight','w')
for doc in result:
	output.write('0'+' ')
	for i in range(0, len(doc)):
		if doc[i] != 0:
			output.write(str(i)+':'+str(doc[i])+" ")
	output.write('\n')
