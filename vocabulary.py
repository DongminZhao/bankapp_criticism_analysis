# -*- coding:utf-8 -*-
from wordcloud import WordCloud
import jieba.analyse
import codecs
import jieba
from collections import Counter
import pandas as pd
from PIL import Image
import numpy as np


def draw_wordcloud(output, name,  dpi=10):
	# 读入一个txt文件
	comment_text = open(output, 'r', encoding="utf8").read()
	# 结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
	cut_text = " ".join(jieba.cut(comment_text))
	image = Image.open(r'./lib/timg.jpg')
	img = np.array(image)
	cloud = WordCloud(
		# 设置字体，不指定就会出现乱码
		font_path="./lib/simfang.ttf",
		# font_path=path.join(d,'simsun.ttc'),
		# 设置背景色
		background_color='white',
		# 词云形状
		# mask=color_mask,
		# 允许最大词汇
		max_words=2000,
		# 最大号字体
		max_font_size=40,
		scale=dpi,
		# stopwords=self.delFile
		mask=img
	)
	word_cloud = cloud.generate(cut_text)
	# 产生词云
	word_cloud.to_file("./output_jpg/cloud_" + name + ".jpg")
	return word_cloud


def split_sentence(cut, infile, jiabafile):
	jieba.analyse.set_stop_words(cut)
	fin = open(infile, 'r', encoding='utf-8', errors='ignore')
	fout = open(jiabafile, 'w', encoding='utf-8')
	for line in fin:
		line = line.strip()
		line = jieba.analyse.extract_tags(line)
		outstr = " ".join(line)
		# print(outstr)
		fout.write(outstr + '\n')

	fin.close()
	fout.close()


def get_words(cut, jiabafile, output, count=1000):
	jieba.analyse.set_stop_words(cut)
	with codecs.open(jiabafile, 'r', 'utf8') as f:
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
		print('%s%s %s  %d' % ('  '*(5-len(k)), k, '*' * 10, v))
		array1.append(k.lower())
		array2.append(v)
	pd.DataFrame({"词语": array1, "频率": array2}).to_csv(output)
	return pd.DataFrame({"词语": array1, "频率": array2})


if __name__ == '__main__':
	split_sentence()
	get_words(20)

