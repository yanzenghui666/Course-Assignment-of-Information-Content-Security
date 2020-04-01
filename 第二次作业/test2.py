# -*- coding: UTF-8 -*-
import os
import re

# 获取每个邮件的存放地址
def getfilesPath(path):
    filesPath = []
    for root, dirs, files in os.walk(path):
        for file in files:
            eachPath = str(root + '\\' + file)
            filesPath.append(eachPath)
    return filesPath

# 提取邮件中的关键词
def getKeyWords(path):
    with open(path, 'r') as f:
        content = f.read()
    content = re.sub("[^A-Za-z]", " ", content)
    content = content.lower()
    content = content.split(" ")
    keyWords = [word for word in content if len(word) > 2]
    return keyWords

# 获取每个邮件的关键词
def getWord(path):
    wordList = [];
    emailPaths = getfilesPath(path)
    for emailPath in emailPaths:
        keyWords = getKeyWords(emailPath)
        wordList.append(keyWords)
    return wordList

# 计算正常/垃圾邮件中每个单词的概率
def getPro(hamWordList, spamWordList):
    hamPros = {}
    spamPros = {}
    unionList = set([i for j in hamWordList for i in j]+[i for j in spamWordList for i in j])
    for word in unionList:
        hamCount = 0
        spamCount = 0
        for hamWord in hamWordList:
            if word in hamWord:
                hamCount += 1
            else:
                continue
        for spamWord in spamWordList:
            if word in spamWord:
                spamCount += 1
            else:
                continue
        hamPro = 0.0
        spamPro = 0.0
        if hamCount != 0:
            hamPro = hamCount/len(hamWordList)
        else:
            hamPro = 0.01
        hamPros[word] = hamPro
        if spamCount != 0:
            spamPro = spamCount/len(spamWordList)
        else:
            spamPro = 0.01
        spamPros[word] = spamPro
    return hamPros, spamPros

# 计算某个单词存在情况下是垃圾邮件的概率
def getPsw(hamPros, spamPros, testPath):
    p = {}
    emailSpamPro = 0.0
    ph = 0.5
    ps = 0.5
    words = getKeyWords(testPath)
    for word in words:
        psw = 0.0
        if word not in spamPros:
            psw = 0.4
        else:
            pwh = hamPros[word]
            pws = spamPros[word]
            psw = ps*pws/(ph*pwh+ps*pws)
        p[word] = psw
    return p

# 计算联合概率
def getJointPro(p):
    pro1 = 1
    pro2 = 1
    for i, j in p.items():
        pro1 *= j
        pro2 *= (1-j)
    jointPro = round(pro1/(pro1+pro2))
    return jointPro

# 获取测试结果
def getResult(hamWordList, spamWordList, testFiles):
    hamPros, spamPros = getPro(hamWordList, spamWordList)
    print(testFiles)
    for testPath in getfilesPath(testFiles):
        p = getPsw(hamPros, spamPros, testPath)
        jointPro = getJointPro(p)
        if jointPro > 0.5:
            print(testPath, ": spam")
        else:
            print(testPath, ": ham")

hamFiles = r"email\ham"
spamFiles = r"email\spam"
testFiles = r"email\test"
getResult(getWord(hamFiles), getWord(spamFiles), testFiles)