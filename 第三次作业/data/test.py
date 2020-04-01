# -*- coding:utf-8 -*-
import os
import jieba
import jieba.analyse
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from pylab import *

# 提取关键词
def getKeyWords(path):
    wordsList = []  # 存储关键词
    wordsDic = {}   # 存储关键词编号
    for fileName in os.listdir(path):
        with open(path+fileName) as f:
            text = f.read() # 读取文本
            keyWords = jieba.analyse.extract_tags(text, topK = 5)   # 提取关键词
            wordsList.append(keyWords)
            for keyWord in keyWords:
                wordsDic[keyWord] = 0
    # 为关键词编号
    for (keyWord, seqNo) in zip(wordsDic, range(len(wordsDic))) :
        wordsDic[keyWord] = seqNo
    return wordsList, wordsDic

# 创建训练文本与关键词矩阵，行为文本，列为关键词
def getTrainMatrix(wordsTrainList, wordsTrainDic):
    wordMatrix = np.zeros([len(wordsTrainList), len(wordsTrainDic)])
    for (index, words) in zip(range(len(wordsTrainList)), wordsTrainList):
        for word in words:
            wordMatrix[index, wordsTrainDic[word]] = 1
    return wordMatrix

# 选择聚类数量
def getClusterNumber(wordsTrainMatrix):
    num = 8 # 设定聚类初始值
    times = 100 # 设定聚类训练次数
    dist = []
    for i in range(1, num):
        minDis = -1
        for j in range(times):
            # 调用sklearn库中的kmeans方法
            kmeans = KMeans(n_clusters = i).fit(wordsTrainMatrix)
            centers = np.array([kmeans.cluster_centers_[k] for k in kmeans.labels_])
            dis = ((wordsTrainMatrix - centers) ** 2).sum()   # 距离（为方便起见不做平方处理）
            minDis = dis if minDis < 0 else min(minDis, dis)
        dist.append(minDis)
    # 绘图
    plot(range(1, num), dist)
    grid()
    show()

# 训练模型
def getModel(wordsTrainMatrix, times, centerNum):
    minDis = -1
    for j in range(times) :
        kmeans = KMeans(n_clusters = centerNum).fit(wordsTrainMatrix)
        centers = np.array([kmeans.cluster_centers_[k] for k in kmeans.labels_])
        dis = ((wordsTrainMatrix - centers) ** 2).sum()
        if minDis < 0 or dis < minDis :
            minDis, testKmeans = dis, kmeans
    return testKmeans

# 创建测试文本与关键词矩阵，行为文本，列为关键词
def getTestMatrix(wordsTrainDic, wordsTrainMatrix, wordsTestList):
    testMatrix = np.zeros([len(wordsTestList), wordsTrainMatrix.shape[1]])
    for (index, keyWords) in zip(range(len(wordsTestList)), wordsTestList):
        for keyWord in keyWords:
            if keyWord in wordsTrainDic:
                testMatrix[index, wordsTrainDic[keyWord]] = 1
    return testMatrix

if __name__ == '__main__':
    trainPath = 'train/C4-Literature/'
    testPath = 'test/C4-Literature/'
    # 提取关键词
    wordsTrainList, wordsTrainDic = getKeyWords(trainPath)
    wordsTestList, wordsTestDic = getKeyWords(testPath)
    # 创建训练文本与关键词矩阵
    wordsTrainMatrix = getTrainMatrix(wordsTrainList, wordsTrainDic)
    # 选择聚类数量
    getClusterNumber(wordsTrainMatrix)
    centerNum = int(input("请输入聚类中心数："))
    # 训练模型
    times = 10  # 训练次数
    testKmeans = getModel(wordsTrainMatrix, times, centerNum)
    # 评价模型
    siCoScore = silhouette_score(wordsTrainMatrix, testKmeans.labels_, metric='euclidean')
    print('轮廓系数:', siCoScore)
    # 模型应用
    fileName = os.listdir(testPath)
    # 创建测试文本与关键词矩阵
    wordsTestMatrix = getTestMatrix(wordsTrainDic, wordsTrainMatrix, wordsTestList)
    print(wordsTestMatrix)
    result = testKmeans.predict(wordsTestMatrix)
    for i in range(result.shape[0]) :
        print (fileName[i] + ',类别:', result[i])