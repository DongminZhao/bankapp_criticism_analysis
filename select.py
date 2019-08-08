import jieba
from collections import Counter
import pandas as pd
import codecs


def select_word(word1="", word2="", word3="", word4="", word5="", path=""):
    output = open(r"./select/output_"+word1+word2+word3+word4+word5+".txt", 'w', encoding='utf-8')
    with open(path, 'r', encoding='utf-8') as f:
        count = 1
        while True:
            tmp = f.readline()
            if word1 in tmp and word2 in tmp and word3 in tmp and word4 in tmp and word5 in tmp:
                print(tmp)
                print("*"*30+str(count))
                count += 1
                output.write(tmp+"\n")
            if not f.readline():
                break
    output.close()
# 简易的关键词搜索


def select_len(num=100, path=""):
    with open(path, 'r', encoding='utf-8') as f:
        while True:
            tmp = f.readline()
            if len(tmp) >= num:
                print(tmp)
                print("*"*30)
            if not f.readline():
                break
# 打印评论


def get_words(path, count=30):
    with codecs.open(path, 'r', 'utf8') as f:
        txt = f.read()
    seg_list = jieba.cut(txt)
    c = Counter()
    for x in seg_list:
        if len(x) > 1 and x != '\n':
            c[x] += 1
    print('常用词频度统计结果')
    array1 = []
    array2 = []
    for (k, v) in c.most_common(count):
        print('%s%s %s  %d' % ('  ' * (5 - len(k)), k, '*' * 10, v))
        array1.append(k.lower())
        array2.append(v)
    pd.DataFrame({"词语": array1, "频率": array2}).to_csv("./select/out_put_jieba_.csv")
# 统计评论中词语的频率


def count_times():
    count = 0
    with open(r"C:\Users\11984\Desktop\phbank_评论爬虫\output_comment\总评论_总评论.txt",
              'r', encoding='utf-8') as f:
        count += len(f.readlines())
    print("共{}条".format(count))
# 统计评论数量


if __name__ == '__main__':
    key = "网络"
    select_word(word1=key, path="")
