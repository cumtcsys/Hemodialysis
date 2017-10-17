# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib
#import matplotlib.pyplot as plt
#from datetime import datetime
#import sys
#from statsmodels.tsa.stattools import adfuller as ADF
#from statsmodels.stats.diagnostic import acorr_ljungbox
#from statsmodels.tsa.arima_model import ARIMA
import patsy
import pandas
import numpy
#from lifelines import CoxPHFitter
#from lifelines.utils import k_fold_cross_validation, concordance_index
#import deepsurv
from deepsurv import DeepSurv
#import lasagne

# self是指调用时的类的实例。
class DataProcess(object):
    def __init__(self):
        self.item = None
        self.patient = None
        self.record = None
        self.excel = None
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
    
    
        # if not self.item or not self.patient or not self.record or not self.excel:

    ###################################################################################################################################
    
    
    
    
    

    
    
    

if __name__ == '__main__':
    dp = DataProcess()
#    dp.load_data()                  # 导入原始数据
#    dp.cut_data_amount_and_attrs()  # 数量规约、属性规约：删除冗余信息、删除无关信息
#    dp.missing_abnormal()           # 缺失和异常处理
#    dp.balance_data()               # 自定义处理，主要是避免分析时出错
    # dp.show_data()
    # dp.merge_and_fill_item()
    # dp.item_stats()         
    # dp.build_dataset1()             # 构建小数据集
#     dp.build_dataset2()             # 构建大数据集
    #
    #
    # dp.linear_small(True)           # 小数据集线性（死亡事件）
    # dp.linear_small(False)          # 小数据集线性（心脑血管事件）
#    dp.deep_small(True)             # 小数据集深度（死亡事件）
    # dp.deep_small(False)            # 小数据集深度（心脑血管事件）

    dp.linear_big(True)             # 大数据集线性（死亡事件）
#    dp.linear_big(False)            # 大数据集线性（心脑血管事件）
#    dp.deep_big(True)               # 大数据集深度（死亡事件）
#    dp.deep_big(False)              # 大数据集深度（心脑血管事件）
    
    # dp.deep_small_train(True)       # 超参数搜索（小数据集）（死亡事件）
    # dp.deep_small_train(False)      # 超参数搜索（小数据集）（心脑血管事件）
    # dp.deep_big_train(True)         # 超参数搜索（大数据集）（死亡事件）
#    dp.deep_big_train(False)        # 超参数搜索（大数据集）（心脑血管事件）
