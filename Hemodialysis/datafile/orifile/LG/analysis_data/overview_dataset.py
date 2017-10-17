# -*- coding: utf-8 -*-
# __future__模块:在旧的版本中试验新版本的一些特性

from __future__ import print_function
import pandas as pd

# 'r'是防止字符转义
dataset1_file = r'dataset1.csv'
dataset2_file = r'dataset2.csv'

# index_col:用作行索引的列编号或者列名
dataset1 = pd.read_csv(dataset1_file, encoding='UTF-8', index_col=[0])
dataset2 = pd.read_csv(dataset2_file, encoding='UTF-8', index_col=[0])

# dataset1['ablocker'] = dataset1[u'\u03b1blocer']
# dataset1['bblocker'] = dataset1[u'\u03b2blocker']
# del dataset1[u'\u03b1blocer']
# del dataset1[u'\u03b2blocker']
# dataset2['ablocker'] = dataset2[u'\u03b1blocer']
# dataset2['bblocker'] = dataset2[u'\u03b2blocker']
# del dataset2[u'\u03b1blocer']
# del dataset2[u'\u03b2blocker']
# dataset1.to_csv(dataset1_file, encoding='UTF-8')
# dataset2.to_csv(dataset2_file, encoding='UTF-8')
# exit(0)

print('dataset1 length: %d, columns: %d' % (len(dataset1), len(dataset1.columns)))
print('dataset2 length: %d, columns: %d' % (len(dataset2), len(dataset2.columns)))

# for index, col in enumerate(dataset1.columns):
#     print('[%3d][%s]->[%d]->[%s]->->' % (index+1, col, len(dataset1[col].dropna()), dataset1[col].dtype), *(list(dataset1[col].unique())[:10]))

# dropna()：drop为NaN的数据，默认丢掉只要含有NaN数据的某行
for index, col in enumerate(dataset2.columns):
    print('[%3d][%s]->[%d]->[%s]->->' % (index+1, col, len(dataset2[col].dropna()), dataset2[col].dtype), *(list(dataset2[col].unique())[:10]))

# 运行结果
# dataset1：length: 185, columns: 380
# dataset2 length: 66882, columns: 204
# [  1][tx_id]->[66882]->[int64]->-> 186 187 188 189 190 191 192 193 194 195
# [  2][patient_id]->[66882]->[int64]->-> 405 426 430 432 440 419 462 465 446 427
# ......