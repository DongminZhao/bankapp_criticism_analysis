# -*- coding:utf-8 -*-

# import logging
import logging.config
import configparser
import numpy as np
import random
import codecs
import os

from collections import OrderedDict
# 为字典键值排序

path = os.getcwd()
# 获得当前工作目录

logging.config.fileConfig("logging.conf")
# 配置配置

logger = logging.getLogger()
# 创建对象

# loggerInfo = logging.getLogger("TimeInfoLogger")
# Consolelogger = logging.getLogger("ConsoleLogger")

conf = configparser.ConfigParser()
# 初始化对象（解析参数文件）

conf.read("setting.conf")
trainfile       = os.path.join(path, os.path.normpath(conf.get("filepath", "trainfile")))
wordidmapfile   = os.path.join(path, os.path.normpath(conf.get("filepath", "wordidmapfile")))
thetafile       = os.path.join(path, os.path.normpath(conf.get("filepath", "thetafile")))
phifile         = os.path.join(path, os.path.normpath(conf.get("filepath", "phifile")))
paramfile       = os.path.join(path, os.path.normpath(conf.get("filepath", "paramfile")))
topNfile        = os.path.join(path, os.path.normpath(conf.get("filepath", "topNfile")))
tassginfile     = os.path.join(path, os.path.normpath(conf.get("filepath", "tassginfile")))
# 拼接地址，‘normpath’：规范化地址

alpha   = float(conf.get("model_args", "alpha"))
beta    = float(conf.get("model_args", "beta"))
K               = int(conf.get("model_args", "K"))
iter_times      = int(conf.get("model_args", "iter_times"))
top_words_num   = int(conf.get("model_args", "top_words_num"))


class Document(object):
    def __init__(self):
        self.words = []
        self.length = 0
# 结构体：文档内容和其长度


class DataPreProcessing(object):

    def __init__(self):
        self.docs_count = 0
        self.words_count = 0
        self.docs = []
        self.word2id = OrderedDict()
        # OrderedDict 为字典键值排序

    def cachewordidmap(self):
        with codecs.open(wordidmapfile, 'w', 'utf-8') as f:
            for word, Id in self.word2id.items():
                f.write(word + "\t" + str(Id) + "\n")
# 写 wordidmapfile


class LDAModel(object):
    
    def __init__(self, dpre):

        self.dpre           = dpre
        self.K              = K
        self.beta           = beta
        self.alpha          = alpha
        self.iter_times     = iter_times
        self.top_words_num  = top_words_num
        self.wordidmapfile  = wordidmapfile
        self.trainfile      = trainfile
        self.thetafile      = thetafile
        self.phifile        = phifile
        self.topNfile       = topNfile
        self.tassginfile    = tassginfile
        self.paramfile      = paramfile

        self.p      = np.zeros(self.K)
        # 1*K
        self.nw     = np.zeros((self.dpre.words_count, self.K), dtype="int")
        # 统计词数*K
        self.nwsum  = np.zeros(self.K, dtype="int")
        # 1*K
        self.nd     = np.zeros((self.dpre.docs_count, self.K), dtype="int")
        # 统计行数*K
        self.ndsum  = np.zeros(dpre.docs_count, dtype="int")
        # 1*统计词数
        self.Z      = np.array([[0 for y in range(dpre.docs[x].length)] for x in range(dpre.docs_count)])
        # 统计行数*统计词数

        # ‘np.zeros’：返回给定形状和类型用0填充

        for x in range(len(self.Z)):
            self.ndsum[x] = self.dpre.docs[x].length
            for y in range(self.dpre.docs[x].length):
                topic = random.randint(0, self.K-1)
                self.Z[x][y] = topic
                self.nw[self.dpre.docs[x].words[y]][topic] += 1
                self.nd[x][topic] += 1
                self.nwsum[topic] += 1

        self.theta = np.array([[0.0 for y in range(self.K)] for x in range(self.dpre.docs_count) ])
        self.phi = np.array([[0.0 for y in range(self.dpre.words_count)] for x in range(self.K)])
        # 定义训练矩阵

    def sampling(self, i, j):

        topic = self.Z[i][j]
        word = self.dpre.docs[i].words[j]
        self.nw[word][topic] -= 1
        self.nd[i][topic] -= 1
        self.nwsum[topic] -= 1
        self.ndsum[i] -= 1

        Vbeta = self.dpre.words_count * self.beta
        Kalpha = self.K * self.alpha
        self.p = (self.nw[word] + self.beta)/(self.nwsum + Vbeta) * \
                 (self.nd[i] + self.alpha) / (self.ndsum[i] + Kalpha)
        
        p = np.squeeze(np.asarray(self.p/np.sum(self.p)))
        topic = np.argmax(np.random.multinomial(1, p))

        self.nw[word][topic] += 1
        self.nwsum[topic] += 1
        self.nd[i][topic] += 1
        self.ndsum[i] += 1

        return topic
    
    def est(self):
        for x in range(self.iter_times):
            for i in range(self.dpre.docs_count):
                for j in range(self.dpre.docs[i].length):
                    topic = self.sampling(i, j)
                    self.Z[i][j] = topic
        logger.info(u"迭代完成。")
        logger.debug(u"计算文章-主题分布")
        self._theta()
        logger.debug(u"计算词-主题分布")
        self._phi()
        logger.debug(u"保存模型")
        self.save()
    
    def _theta(self):
        for i in range(self.dpre.docs_count):
            self.theta[i] = (self.nd[i]+self.alpha)/(self.ndsum[i]+self.K * self.alpha)
    
    def _phi(self):
        for i in range(self.K):
            self.phi[i] = (self.nw.T[i] + self.beta)/(self.nwsum[i]+self.dpre.words_count * self.beta)
    
    def save(self):
        logger.info(u"文章-主题分布已保存到%s" % self.thetafile)
        
        with codecs.open(self.thetafile, 'w') as f:
            for x in range(self.dpre.docs_count):
                for y in range(self.K):
                    f.write(str(self.theta[x][y]) + '\t')
                f.write('\n')
        
        logger.info(u"词-主题分布已保存到%s" % self.phifile)
        
        with codecs.open(self.phifile, 'w') as f:
            for x in range(self.K):
                for y in range(self.dpre.words_count):
                    f.write(str(self.phi[x][y]) + '\t')
                f.write('\n')
        
        logger.info(u"参数设置已保存到%s" % self.paramfile)
        
        with codecs.open(self.paramfile, 'w', 'utf-8') as f:
            f.write('K=' + str(self.K) + '\n')
            f.write('alpha=' + str(self.alpha) + '\n')
            f.write('beta=' + str(self.beta) + '\n')
            f.write(u'迭代次数  iter_times=' + str(self.iter_times) + '\n')
            f.write(u'每个类的高频词显示个数  top_words_num=' + str(self.top_words_num) + '\n')
        
        logger.info(u"主题topN词已保存到%s" % self.topNfile)

        with codecs.open(self.topNfile, 'w', 'utf-8') as f:
            self.top_words_num = min(self.top_words_num, self.dpre.words_count)
            for x in range(self.K):
                f.write(u'第' + str(x) + u'类：' + '\n')
                twords = []
                twords = [(n, self.phi[x][n]) for n in range(self.dpre.words_count)]
                twords.sort(key=lambda i: i[1], reverse=True)
                for y in range(self.top_words_num):
                    word = OrderedDict({value: key for key, value in self.dpre.word2id.items()})[twords[y][0]]
                    f.write('\t'*2 + word + '\t' + str(twords[y][1]) + '\n')
        
        logger.info(u"文章-词-主题分派结果已保存到%s" % self.tassginfile)
        
        with codecs.open(self.tassginfile, 'w') as f:
            for x in range(self.dpre.docs_count):
                for y in range(self.dpre.docs[x].length):
                    f.write(str(self.dpre.docs[x].words[y])+':'+str(self.Z[x][y]) + '\t')
                f.write('\n')
        
        logger.info(u"模型训练完成。")


def preprocessing():
    logger.info(u'载入数据......')
    with codecs.open(trainfile, 'r', 'utf-8') as f:
        docs = f.readlines()
    # 读已分词数据

    logger.debug(u"载入完成,准备生成字典对象和统计文本数据...")
    # 根据log等级显示

    dpre = DataPreProcessing()
    # 写 wordidmapfile

    items_idx = 0
    for line in docs:
        if line != "":
            tmp = line.strip().split()

            doc = Document()
            # 初始化对象 结构体：文档内容和其长度

            for item in tmp:
                if item in dpre.word2id:
                    # 存在+1
                    doc.words.append(dpre.word2id[item])
                else:
                    # 不存在创建
                    dpre.word2id[item] = items_idx
                    doc.words.append(items_idx)
                    items_idx += 1
            doc.length = len(tmp)
            dpre.docs.append(doc)
        else:

            pass

    dpre.docs_count = len(dpre.docs)
    dpre.words_count = len(dpre.word2id)
    logger.info(u"共有%s个文档" % dpre.docs_count)
    dpre.cachewordidmap()
    logger.info(u"词与序号对应关系已保存到%s" % wordidmapfile)
    return dpre


def run():
    dpre = preprocessing()

    lda = LDAModel(dpre)
    lda.est()


# if __name__ == '__main__':
#     run()
