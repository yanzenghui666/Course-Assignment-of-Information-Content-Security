# -*- coding: UTF-8 -*-
import jieba
import re
from collections import defaultdict
import math
import operator

"""
函数：加载数据
参数：TXT文件地址（字符串）
返回：TXT文件内容（字符串）
"""
def lodaData(address):
    file = open(address,"r")
    str = file.read()
    file.close()
    str = re.sub('\W+', '', str)    # 正则表达式去标点符号
    return str

"""
函数：TF-IDF算法
参数：分析内容（数组）
返回：分析结果（数组）
"""
def feature_select(list_words):
    # 统计词频
    docs_frequency = []
    for index in range(len(list_words)):
        doc_frequency = defaultdict(int);
        for word in list_words[index]:
            doc_frequency[word] += 1
        docs_frequency.append(doc_frequency)

    # 计算TF
    for doc_frequency in docs_frequency:
        for word_frequency in doc_frequency:
            doc_frequency[word_frequency] /= len(doc_frequency)
    
    # 计算IDF
    word_doc = defaultdict(int) # 存储包含该词的文档数
    for doc_frequency in docs_frequency:
        for word_frequency in doc_frequency:
            word_doc[word_frequency] += 1
    for word in word_doc:
        word_doc[word] = abs(math.log(4/(word_doc[word]+1)))
    
    # 计算TF-IDF
    for doc_frequency in docs_frequency:
        for word_frequency in doc_frequency:
            doc_frequency[word_frequency] *= word_doc[word_frequency]
    
    # 按字典值由大到小排序
    result = [];
    for doc_frequency in docs_frequency:
        doc_frequency = sorted(doc_frequency.items(),key=operator.itemgetter(1),reverse=True)
        result.append(doc_frequency[0][0])
        
    return result

list_words = []
list_words.append(jieba.lcut(lodaData("语料库/2015.txt")))
list_words.append(jieba.lcut(lodaData("语料库/2016.txt")))
list_words.append(jieba.lcut(lodaData("语料库/2017.txt")))
list_words.append(jieba.lcut(lodaData("语料库/2018.txt")))
result = (feature_select(list_words))
file = open("result.txt","w")
str = file.write("2015:"+result[0]+"\n")
str = file.write("2016:"+result[1]+"\n")
str = file.write("2017:"+result[2]+"\n")
str = file.write("2018:"+result[3]+"\n")
file.close()