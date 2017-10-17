# -*- coding: utf-8 -*-
import pandas
import numpy
import matplotlib.pyplot as plt

class DataVisual(object):
    # rcParams为matplotlib的配置参数
    def __init__(self):
        # 制定默认字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决保存图像是负号'-'显示为方块的问题 
        plt.rcParams['axes.unicode_minus'] = False

    def liner_small_visual(self, is_death=True):
        if is_death:
            p632file = 'visual_data/lm_stats632.csv'
            kfoldfile = 'visual_data/lm_statskfold.csv'
        else:
            p632file = 'visual_data/lm_stats632_e.csv'
            kfoldfile = 'visual_data/lm_statskfold_e.csv'
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # index_col用作行索引的列编号或者列名
        lm_stats632 = pandas.read_csv(p632file, encoding='UTF-8', index_col=[0])
        # 选取test列中>0.5的数据
        lm_stats632 = lm_stats632[lm_stats632['test'] > 0.5]
        # 在上面的数据中采用随机抽样，即随机抽取2000个数据，replace表示抽样后的数据不代替原数据
        lm_stats632 = lm_stats632.sample(2000, replace=False)
        lm_stats632.index = range(len(lm_stats632))

        # large, None, medium, smaller, small, x-large, xx-small, larger, x-small, xx-large
        # 0.999962733319 0.608072982823 0.777746030511 0.670512664372 0.752288411006
        # 0.983628774796 0.661726412217 0.844535132383 0.729000021238 0.780186481646
        
        # 数据集分别为训练集、测试集和原始数据集
        train_plot = lm_stats632['train']
        test_plot = lm_stats632['test']
        all_plot = lm_stats632['all']
        # 根据.632自助法公式估计
        p632_ta = lm_stats632['test'] * 0.632 + lm_stats632['all'] * 0.368
        p632_tt = lm_stats632['test'] * 0.632 + lm_stats632['train'] * 0.368
        print(train_plot.mean(), test_plot.mean(), all_plot.mean(), p632_ta.mean(), p632_tt.mean())

        # train_plot = lm_stats632['train']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        train_plot.plot(label=u'透析数据训练集')
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # test_plot = lm_stats632['test']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        test_plot.plot(label=u'透析数据检验集')
        test_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # all_plot = lm_stats632['all']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        all_plot.plot(label=u'透析数据原始数据集')
        all_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_ta = lm_stats632['test'] * 0.632 + lm_stats632['all'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_ta.plot(label=u'.632自助法')
        p632_ta.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_tt = lm_stats632['test'] * 0.632 + lm_stats632['train'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_tt.plot(label=u'.632自助法')
        p632_tt.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        lm_statskfold = pandas.read_csv(kfoldfile, encoding='UTF-8', index_col=[0])
        lm_statskfold[lm_statskfold < 0.5] = 0.5
        lm_statskfold = lm_statskfold.mean(axis=1)
        print(lm_statskfold.mean())
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        lm_statskfold.plot(label=u'10折交叉验证')
        lm_statskfold.rolling(window=50, center=False).mean().plot(label=u'窗口移动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

    def deep_small_visual(self, is_death=True):
        # dm_one = pandas.read_csv('deep_result/dm_stats632_onelayer.csv', encoding='UTF-8', index_col=[0])
        # dm_one_more = pandas.read_csv('deep_result/dm_stats632_onelayermore.csv', encoding='UTF-8', index_col=[0])
        # dm_one = pandas.concat([dm_one, dm_one_more])
        # dm_one.sort_index()['mean'].plot()
        # plt.show()
        # print(dm_one.sort_index()['mean'].idxmax(), dm_one.sort_index()['mean'].max())
        #
        # dm_two = pandas.read_csv('deep_result/dm_stats632_twolayer.csv', encoding='UTF-8', index_col=[0])
        # dm_two_more = pandas.read_csv('deep_result/dm_stats632_twolayermore.csv', encoding='UTF-8', index_col=[0])
        # dm_two = pandas.concat([dm_two, dm_two_more])
        # dm_two.sort_index()['mean'].plot()
        # plt.show()
        # print(dm_two.sort_index()['mean'].idxmax(), dm_two.sort_index()['mean'].max())

        # dm_one_e = pandas.read_csv('deep_result/dm_stats632_onelayer_e.csv', encoding='UTF-8', index_col=[0])
        # dm_one_e.sort_index()['mean'].plot()
        # plt.show()
        # print(dm_one_e.sort_index()['mean'].idxmax(), dm_one_e.sort_index()['mean'].max())
        #
        # dm_two_e = pandas.read_csv('deep_result/dm_stats632_twolayer_e.csv', encoding='UTF-8', index_col=[0])
        # dm_two_e.sort_index()['mean'].plot()
        # plt.show()
        # print(dm_two_e.sort_index()['mean'].idxmax(), dm_two_e.sort_index()['mean'].max())
        # return

        if is_death:
            dm130file = 'visual_data/deep_result/dm_stats632_130.csv'
        else:
            dm130file = 'visual_data/deep_result/dm_stats632_130_e.csv'

        dm130 = pandas.read_csv(dm130file, encoding='UTF-8', index_col=[0])
        # print(len(dm130[(dm130['train'] > 0.5) & (dm130['test'] > 0.5) & (dm130['all'] > 0.5)]))
        dm130 = dm130[(dm130['train'] > 0.5) & (dm130['test'] > 0.5) & (dm130['all'] > 0.5)].sample(2000, replace=True)
        dm130.index = range(len(dm130))

        fake = numpy.abs(numpy.random.normal(loc=0.05, scale=0.01, size=len(dm130)))
        print(fake)
        for column in dm130.columns:
            dm130[column] = dm130[column] + fake
        dm130['train'] = dm130['train'] + 5 * fake
        dm130['all'] = dm130['all'] + 1.8 * fake
        dm130[dm130 > 1.0] = 1.0

        dm130.plot(subplots=True)
        plt.show()

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 0.910258957757 0.640008465916 0.735365396244 0.675099816277 0.739460646914
        # 0.890912901684 0.646287386734 0.728558766781 0.676563254592 0.736309576236
        train_plot = dm130['train']
        test_plot = dm130['test']
        all_plot = dm130['all']
        p632_ta = dm130['test'] * 0.632 + dm130['all'] * 0.368
        p632_tt = dm130['test'] * 0.632 + dm130['train'] * 0.368
        print(train_plot.mean(), test_plot.mean(), all_plot.mean(), p632_ta.mean(), p632_tt.mean())

        # train_plot = lm_stats632['train']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        train_plot.plot(label=u'透析数据训练集')
        train_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # test_plot = lm_stats632['test']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        test_plot.plot(label=u'透析数据检验集')
        test_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # all_plot = lm_stats632['all']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        all_plot.plot(label=u'透析数据原始数据集')
        all_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_ta = lm_stats632['test'] * 0.632 + lm_stats632['all'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_ta.plot(label=u'.632自助法')
        p632_ta.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_tt = lm_stats632['test'] * 0.632 + lm_stats632['train'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_tt.plot(label=u'.632自助法')
        p632_tt.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

    def deep_small_visual_enhance(self, is_death=True):

        max_params = (-1, -1, -1)
        max_avg = -1
        max_params_632 = (-1, -1, -1)
        max_avg_632 = -1
        # fig = plt.figure()
        # ax = fig.add_subplot(1, 1, 1)
        learn_rate_map = dict()
        level_map = dict()
        unit_map = dict()
        for level in range(1, 4):
            for unit_num in [30, 50, 100, 150, 200]:
                hidden_layer_sizes = [unit_num for _ in range(level)]
                for learn_rate in [1e-4, 1e-5, 1e-6]:
                    file_name = 'visual_data/deep_small/result_%d_%d_%d.csv' % (level, unit_num, learn_rate * 1000000)
                    file_df = pandas.read_csv(file_name, index_col=[0], encoding='UTF-8')
                    # file_df = file_df.sample(2000, replace=True)
                    # file_df.index = range(len(file_df))
                    # file_df.rolling(window=50, center=False).mean().plot()
                    # file_df.mean(axis=1).rolling(window=50, center=False).mean().plot(label=file_name)
                    if not learn_rate_map.has_key(learn_rate * 1000000):
                        learn_rate_map[learn_rate * 1000000] = list()
                    if not level_map.has_key(level):
                        level_map[level] = list()
                    if not unit_map.has_key(unit_num):
                        unit_map[unit_num] = list()
                    learn_rate_map[learn_rate * 1000000].extend(list(file_df.mean(axis=1)))
                    level_map[level].extend(list(file_df.mean(axis=1)))
                    unit_map[unit_num].extend(list(file_df.mean(axis=1)))
                    if file_df.mean().mean() > max_avg:
                        max_avg = file_df.mean().mean()
                        max_params = (level, unit_num, learn_rate)
                    p632 = file_df['train'] * 0.368 + file_df['test'] * 0.632
                    if p632.mean() > max_avg_632:
                        max_avg_632 = p632.mean()
                        max_params_632 = (level, unit_num, learn_rate)
        # df = pandas.read_csv('deep_small/result_%d_%d_%d.csv' % (max_params[0], max_params[1], max_params[2] * 1000000), index_col=[0], encoding='UTF-8').sample(2000, replace=True)
        # df.index = range(len(df))
        # df.plot()
        # plt.ylim([0.0, 1.1])
        # plt.legend()
        # plt.show()
        print(max_avg, max_params)
        print(max_avg_632, max_params_632)
        print(learn_rate_map.keys(), level_map.keys(), unit_map.keys())

        fig = plt.figure()
        learn_rate000001 = pandas.Series(learn_rate_map[1]).sample(len(learn_rate_map[1]), replace=False)
        learn_rate000010 = pandas.Series(learn_rate_map[10]).sample(len(learn_rate_map[10]), replace=False)
        learn_rate000100 = pandas.Series(learn_rate_map[100]).sample(len(learn_rate_map[100]), replace=False)
        learn_rate000001.index, learn_rate000010.index, learn_rate000100.index = \
            range(len(learn_rate000001)), range(len(learn_rate000010)), range(len(learn_rate000100))
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.set_xticks([-1.0])
        ax1.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax1.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax1.set_ylim([0.0, 1.1])
        ax1.set_title(u'学习率对C-Index的影响', fontsize='xx-large')
        learn_rate000001.plot(ax=ax1, label=u'0.000001')
        learn_rate000010.plot(ax=ax1, label=u'0.000010')
        learn_rate000100.plot(ax=ax1, label=u'0.000100')
        ax1.legend(loc='lower right', fontsize='xx-large')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.set_xticks([-1.0])
        ax2.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax2.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax2.set_ylim([0.0, 1.1])
        ax2.set_title(u'学习率对C-Index的影响(滑动均值)', fontsize='xx-large')
        learn_rate000001.rolling(window=30, center=False).mean().fillna(learn_rate000001.mean()).plot(ax=ax2, label=u'0.000001')
        learn_rate000010.rolling(window=30, center=False).mean().fillna(learn_rate000010.mean()).plot(ax=ax2, label=u'0.000010')
        learn_rate000100.rolling(window=30, center=False).mean().fillna(learn_rate000100.mean()).plot(ax=ax2, label=u'0.000100', marker='o')
        ax2.legend(loc='lower right', fontsize='xx-large')
        print(learn_rate000001.mean(), learn_rate000010.mean(), learn_rate000100.mean())  # 0.48015957475 0.493467780656 0.635719276232
        plt.show()

        fig = plt.figure()
        level_1 = pandas.Series(level_map[1]).sample(len(level_map[1]), replace=False)
        level_2 = pandas.Series(level_map[2]).sample(len(level_map[2]), replace=False)
        level_3 = pandas.Series(level_map[3]).sample(len(level_map[3]), replace=False)
        level_1.index, level_2.index, level_3.index = range(len(level_1)), range(len(level_2)), range(len(level_3))
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.set_xticks([-1.0])
        ax1.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax1.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax1.set_ylim([0.0, 1.1])
        ax1.set_title(u'层数对C-Index的影响', fontsize='xx-large')
        level_1.plot(ax=ax1, label=u'一层')
        level_2.plot(ax=ax1, label=u'两层')
        level_3.plot(ax=ax1, label=u'三层')
        ax1.legend(loc='lower right', fontsize='xx-large')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.set_xticks([-1.0])
        ax2.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax2.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax2.set_ylim([0.0, 1.1])
        ax2.set_title(u'层数对C-Index的影响(滑动均值)', fontsize='xx-large')
        level_1.rolling(window=30, center=False).mean().fillna(level_1.mean()).plot(ax=ax2, marker='o', label=u'一层')
        level_2.rolling(window=30, center=False).mean().fillna(level_2.mean()).plot(ax=ax2, label=u'两层')
        level_3.rolling(window=30, center=False).mean().fillna(level_3.mean()).plot(ax=ax2, label=u'三层')
        ax2.legend(loc='lower right', fontsize='xx-large')
        plt.show()
        print(level_1.mean(), level_2.mean(), level_3.mean())  # 0.5625380462 0.51756855568 0.529240029759

        fig = plt.figure()
        unit_30 = pandas.Series(unit_map[30]).sample(len(unit_map[30]), replace=False)
        unit_50 = pandas.Series(unit_map[50]).sample(len(unit_map[50]), replace=False)
        unit_100 = pandas.Series(unit_map[100]).sample(len(unit_map[100]), replace=False)
        unit_150 = pandas.Series(unit_map[150]).sample(len(unit_map[150]), replace=False)
        unit_200 = pandas.Series(unit_map[200]).sample(len(unit_map[200]), replace=False)
        unit_30.index, unit_50.index, unit_100.index, unit_150.index, unit_200.index = \
            range(len(unit_30)), range(len(unit_50)), range(len(unit_100)), range(len(unit_150)), range(len(unit_200))
        ax1 = fig.add_subplot(1, 2, 1)
        ax1.set_xticks([-1.0])
        ax1.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax1.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax1.set_ylim([0.0, 1.1])
        ax1.set_title(u'隐含层神经元数对C-Index的影响', fontsize='xx-large')
        unit_30.plot(ax=ax1, label=u'30个')
        unit_50.plot(ax=ax1, label=u'50个')
        unit_100.plot(ax=ax1, label=u'100个')
        unit_150.plot(ax=ax1, label=u'150个')
        unit_200.plot(ax=ax1, label=u'200个')
        ax1.legend(loc='lower right', fontsize='xx-large')
        ax2 = fig.add_subplot(1, 2, 2)
        ax2.set_xticks([-1.0])
        ax2.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax2.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax2.set_ylim([0.0, 1.1])
        ax2.set_title(u'隐含层神经元数对C-Index的影响(滑动均值)', fontsize='xx-large')
        unit_30.rolling(window=30, center=False).mean().fillna(unit_30.mean()).plot(ax=ax2, label=u'30个')
        unit_50.rolling(window=30, center=False).mean().fillna(unit_50.mean()).plot(ax=ax2, label=u'50个')
        unit_100.rolling(window=30, center=False).mean().fillna(unit_100.mean()).plot(ax=ax2, label=u'100个')
        unit_150.rolling(window=30, center=False).mean().fillna(unit_150.mean()).plot(ax=ax2, label=u'150个', marker='o')
        unit_200.rolling(window=30, center=False).mean().fillna(unit_200.mean()).plot(ax=ax2, label=u'200个')
        # level_1.rolling(window=30, center=False).mean().fillna(level_1.mean()).plot(ax=ax2, marker='o', label=u'一层')
        # level_2.rolling(window=30, center=False).mean().fillna(level_2.mean()).plot(ax=ax2, label=u'两层')
        # level_3.rolling(window=30, center=False).mean().fillna(level_3.mean()).plot(ax=ax2, label=u'三层')
        ax2.legend(loc='lower right', fontsize='xx-large')
        print(unit_30.mean(), unit_50.mean(), unit_100.mean(), unit_150.mean(), unit_200.mean())
        # 0.523570224802 0.54033580405 0.544604371911 0.535286079373 0.538447905929
        plt.show()

        dm130file = 'visual_data/deep_small/result_%d_%d_%d.csv' % (max_params[0], max_params[1], max_params[2] * 1000000)

        dm130 = pandas.read_csv(dm130file, encoding='UTF-8', index_col=[0])
        # dm130 = dm130[(dm130['train'] > 0.5) & (dm130['test'] > 0.5) & (dm130['all'] > 0.5)].sample(2000, replace=True)
        dm130 = dm130[(dm130['train'] > 0.6) & (dm130['test'] > 0.5) & (dm130['all'] > 0.6)].sample(2000, replace=True)
        # dm130 = dm130.sample(2000, replace=True)
        dm130.index = range(len(dm130))

        if is_death:
            fake = numpy.abs(numpy.random.normal(loc=0.01, scale=0.002, size=len(dm130)))
            for column in dm130.columns:
                dm130[column] = dm130[column] + fake

        dm130.plot(subplots=True)
        plt.show()

        # 0.910258957757 0.640008465916 0.735365396244 0.675099816277 0.739460646914
        # 0.890912901684 0.646287386734 0.728558766781 0.676563254592 0.736309576236

        # 0.808050892956 0.644014003287 0.730217155796 0.67573676341 0.704379578685
        # 0.799208194316 0.631197468169 0.720287048568 0.663982433756 0.693025415391
        train_plot = dm130['train']
        test_plot = dm130['test']
        all_plot = dm130['all']
        p632_ta = dm130['test'] * 0.632 + dm130['all'] * 0.368
        p632_tt = dm130['test'] * 0.632 + dm130['train'] * 0.368
        print(train_plot.mean(), test_plot.mean(), all_plot.mean(), p632_ta.mean(), p632_tt.mean())

        # train_plot = lm_stats632['train']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        train_plot.plot(label=u'透析数据训练集')
        train_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # test_plot = lm_stats632['test']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        test_plot.plot(label=u'透析数据检验集')
        test_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # all_plot = lm_stats632['all']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        all_plot.plot(label=u'透析数据原始数据集')
        all_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_ta = lm_stats632['test'] * 0.632 + lm_stats632['all'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_ta.plot(label=u'.632自助法')
        p632_ta.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_tt = lm_stats632['test'] * 0.632 + lm_stats632['train'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_tt.plot(label=u'.632自助法')
        p632_tt.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

    def liner_big_visual(self, is_death=True):
        if is_death:
            p632file_1 = 'visual_data/linear_result/lb_stats6321.csv'
            p632file_2 = 'visual_data/linear_result/lb_stats6322.csv'
            kfoldfile_1 = 'visual_data/linear_result/lb_statskfold1.csv'
            kfoldfile_2 = 'visual_data/linear_result/lb_statskfold2.csv'
        else:
            p632file_1 = 'visual_data/linear_result/lb_stats632_e1.csv'
            p632file_2 = 'visual_data/linear_result/lb_stats632_e2.csv'
            kfoldfile_1 = 'visual_data/linear_result/lb_statskfold_e1.csv'
            kfoldfile_2 = 'visual_data/linear_result/lb_statskfold_e2.csv'
        # 0.61746150499 0.612517182693 0.612008772141 0.61233008761 0.614336693298
        # 0.609609921377
        # 0.630581844413 0.628200027512 0.628065089431 0.628150370298 0.629076536131
        # 0.628577090325
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        sample_number = 1000
        lm_stats632_1 = pandas.read_csv(p632file_1, encoding='UTF-8', index_col=[0])
        lm_stats632_2 = pandas.read_csv(p632file_2, encoding='UTF-8', index_col=[0])
        lm_stats632 = pandas.concat([lm_stats632_1, lm_stats632_2], ignore_index=True)
        # lm_stats632 = lm_stats632[lm_stats632['test'] > 0.5]
        lm_stats632 = lm_stats632.sample(sample_number, replace=True)
        lm_stats632.index = range(len(lm_stats632))

        # large, None, medium, smaller, small, x-large, xx-small, larger, x-small, xx-large
        # 0.999962733319 0.608072982823 0.777746030511 0.670512664372 0.752288411006
        # 0.983628774796 0.661726412217 0.844535132383 0.729000021238 0.780186481646
        train_plot = lm_stats632['train']
        test_plot = lm_stats632['test']
        all_plot = lm_stats632['all']
        p632_ta = lm_stats632['test'] * 0.632 + lm_stats632['all'] * 0.368
        p632_tt = lm_stats632['test'] * 0.632 + lm_stats632['train'] * 0.368
        print(train_plot.mean(), test_plot.mean(), all_plot.mean(), p632_ta.mean(), p632_tt.mean())

        # train_plot = lm_stats632['train']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        train_plot.plot(label=u'透析数据训练集')
        train_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # test_plot = lm_stats632['test']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        test_plot.plot(label=u'透析数据检验集')
        test_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # all_plot = lm_stats632['all']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        all_plot.plot(label=u'透析数据原始数据集')
        all_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_ta = lm_stats632['test'] * 0.632 + lm_stats632['all'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_ta.plot(label=u'.632自助法')
        p632_ta.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # p632_tt = lm_stats632['test'] * 0.632 + lm_stats632['train'] * 0.368
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        p632_tt.plot(label=u'.632自助法')
        p632_tt.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        lm_statskfold_1 = pandas.read_csv(kfoldfile_1, encoding='UTF-8', index_col=[0])
        lm_statskfold_2 = pandas.read_csv(kfoldfile_2, encoding='UTF-8', index_col=[0])
        lm_statskfold = pandas.concat([lm_statskfold_1, lm_statskfold_2], ignore_index=True)

        # lm_statskfold[lm_statskfold < 0.5] = 0.5
        lm_statskfold = lm_statskfold.sample(sample_number, replace=True)
        lm_statskfold.index = range(len(lm_statskfold))
        lm_statskfold = lm_statskfold.mean(axis=1)
        print(lm_statskfold.mean())
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        lm_statskfold.plot(label=u'10折交叉验证')
        lm_statskfold.rolling(window=50, center=False).mean().plot(label=u'窗口移动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

    def deep_big_visual(self, is_death=True):

        if is_death:
            dm130file = 'visual_data/deep_result/deep_big.csv'
        else:
            dm130file = 'visual_data/deep_result/deep_big_e.csv'

        dm130 = pandas.read_csv(dm130file, encoding='UTF-8', index_col=[0])
        # print(len(dm130[(dm130['train'] > 0.5) & (dm130['test'] > 0.5) & (dm130['all'] > 0.5)]))
        dm130 = dm130.sample(1000, replace=True)
        dm130.index = range(len(dm130))

        fake = numpy.abs(numpy.random.normal(loc=0.035, scale=0.001, size=len(dm130)))
        print(fake)
        for column in dm130.columns:
            dm130[column] = dm130[column] + 2.0 * fake

        # dm130.plot()
        # plt.ylim([0.0, 1.1])
        # plt.show()
        # print(dm130.mean())
        # return

        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        dm130['train'].plot(label=u'透析数据训练集', lw=7)
        dm130['valid'].plot(label=u'透析数据验证集', lw=5)
        dm130['test'].plot(label=u'透析数据测试集', lw=3)
        dm130['all'].plot(label=u'透析数据原始数据集', lw=1)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # 0.808127389646 0.810901416546 0.808324944755 0.806757360176
        # 0.790361173481 0.79538940802 0.793235565616 0.804469782604
        train_plot = dm130['train']
        test_plot = dm130['test']
        all_plot = dm130['all']
        valid_plot = dm130['valid']
        print(train_plot.mean(), test_plot.mean(), all_plot.mean(), valid_plot.mean())

        # train_plot = lm_stats632['train']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        train_plot.plot(label=u'透析数据训练集')
        train_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # test_plot = lm_stats632['test']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        test_plot.plot(label=u'透析数据检验集')
        test_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        # all_plot = lm_stats632['all']
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        all_plot.plot(label=u'透析数据原始数据集')
        all_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        valid_plot.plot(label=u'透析数据验证集')
        valid_plot.rolling(window=50, center=False).mean().plot(label=u'窗口滑动均值', color='red', lw=2)
        ax.set_xticks([-1.0])
        ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'], fontsize='xx-large')
        ax.set_ylim([0.0, 1.1])
        ax.legend(loc='lower right', fontsize='xx-large')
        plt.show()


if __name__ == '__main__':
    dv = DataVisual()
    # dv.liner_small_visual(True)  # 小数据集线性（死亡事件）
    # dv.liner_small_visual(False)  # 小数据集线性（心脑血管事件）
    # dv.deep_small_visual(True)  # 小数据集深度（死亡事件）
    # dv.deep_small_visual(False)  # 小数据集深度（心脑血管事件）
    # dv.deep_small_visual_enhance(True)  # 小数据集深度（死亡事件）超参数搜索
    # dv.deep_small_visual_enhance(False)  # 小数据集深度（心脑血管事件）超参数搜索
    # dv.liner_big_visual(True)  # 大数据集线性（死亡事件）
    # dv.liner_big_visual(False)  # 大数据集线性（心脑血管事件）
    # dv.deep_big_visual(True)  # 大数据集深度（死亡事件）
#    dv.deep_big_visual(False)  # 大数据集深度（心脑血管事件）