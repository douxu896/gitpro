#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from sklearn.feature_extraction.text import CountVectorizer

listfile=os.listdir('/home/emily/Desktop/Data/')
txt_arr=[]
print "start do"
for i in range(4):
    txt_content=open('/home/emily/Desktop/Data/'+listfile[i],'rw')

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

# print texts_filtered
#中心词，词元化
wnl = nltk.WordNetLemmatizer()
texts_lemmatized=[[wnl.lemmatize(word) for word in document] for document in texts_filtered]


#去掉低频词
all_stems = sum(texts_lemmatized, [])
stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
texts = [[stem for stem in text if stem not in stems_once] for text in texts_lemmatized]

vec = CountVectorizer(min_df=1, ngram_range=(1,2)) 
x = vec.fit_transform(texts_filtered.toarray())
print x
# print texts
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

#抽取词袋，将文档的token映射为id
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

#TF-IDF模型
tfidf = models.TfidfModel(corpus)
#用词频表示文档向量表示为一个用tf-idf值表示的文档向量
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=20)
corpus_lsi = lsi[corpus_tfidf]
#建索引
index = similarities.MatrixSimilarity(lsi[corpus])

lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=20)

# save model
# lsi.save('model.lsi')

# print lsi, '\n'
# print corpus_lsi, '\n'
# corpus_lsi.print_topics()
# for ids, topic in lsi.print_topics():
#     print 'topic id = ', ids, '\n', topic, '\n'
f = open('modal.txt','w') 
# print tfidf, '\n' # TfidfModel(num_docs=9, num_nnz=51) 
for doc in corpus_tfidf: # convert the whole corpus on the fly
    f.write(str(doc)+" ")
f.close()
    # print doc

    # f.write(str(doc))
# corpus_tfidf.save('modal.txt')




for pic in corpus_lsi:
    print pic
 