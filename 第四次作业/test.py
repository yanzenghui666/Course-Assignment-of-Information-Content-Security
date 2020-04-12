import re
import jieba
import jieba.posseg as poss
from gensim.models import word2vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 读取txt文件
def readFile(path, ways, code):
    with open(path, ways, encoding=code) as f:
        content = f.read()
    return content

# 数据预处理
def processData(content):
    # 去除换行符等特殊字符
    content = re.split('\W+', content)
    # 分词
    content_cut = []
    for i in content:
        content_cut += jieba.lcut(i)
    # 去除停用词
    stop_words = readFile('停用词.txt', 'r', 'utf-8');
    stop_words = re.split('\n', stop_words)
    words = [word for word in content_cut if word not in stop_words]
    return words

# 提取人名
def extractName(content):
    # 数据预处理
    words = processData(content)    
    # 构建词向量
    my_wv = word2vec.Word2Vec(words, size=100, min_count=10, window=3, iter=500)
    # 提取关键词
    content_poss = poss.lcut(content)
    people = [i.word for i in content_poss if i.flag =='nr']
    people = list(set(people))
    # 提取人名
    data = []
    name = []
    for i in people:
        try:
            data.append(my_wv.wv[i])
            name.append(i)
        except KeyError:
            pass
    print(name)
    return name, data

# 可视话
def visualization(name, data):
    # PCA数据降维
    data = PCA(n_components=2).fit_transform(data)
    # 可视化
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置字体为SimHei
    plt.rcParams['axes.unicode_minus'] = False  # 设置正常显示字符
    plt.figure(figsize=(15,15), dpi=360)        # 设置显示的最大范围
    for i in range(len(data)):
        plt.scatter(data[i,0], data[i,1])
        plt.text(data[i,0], data[i,1], name[i])
    # plt.savefig('test.png')    #保存到本地
    plt.show()

    
filePath = '人民的名义人物关系分析/剧情梗概.txt';
content = readFile(filePath, 'r', 'utf-8')
name, data = extractName(content)
visualization(name, data)