# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas
import patsy
import numpy
from deepsurv import DeepSurv
from lifelines import CoxPHFitter
from lifelines.utils import k_fold_cross_validation, concordance_index
import time as Time
class TrainService:
    def __init__(self):
        print("TrainService")
    def deep_big_train_death(self,train_data_path,result_single_dir,result_gather_dir):
        self.__deep_big_train(True,train_data_path,result_single_dir,result_gather_dir)
    def deep_big_train_cds(self,train_data_path,result_single_dir,result_gather_dir):
        self.__deep_big_train(False,train_data_path,result_single_dir,result_gather_dir)
    
    def linear_big_train_death(self,train_data_path,basepath):
        self.__linear_big(True,train_data_path,basepath)
    def linear_big_train_cds(self,train_data_path,basepath):
        self.__linear_big(False,train_data_path,basepath)
    
    def deep_small_train_death(self,train_data_path,result_single_dir,result_gather_dir):
        self.__deep_small_train(True,train_data_path,result_single_dir,result_gather_dir)
    def deep_small_train_cds(self,train_data_path,result_single_dir,result_gather_dir):
        self.__deep_small_train(False,train_data_path,result_single_dir,result_gather_dir)
    
    def linear_small_train_death(self,train_data_path,basepath):
        self.__linear_small(True,train_data_path,basepath)
    def linear_small_train_cds(self,train_data_path,basepath):
        self.__linear_small(False,train_data_path,basepath)
        
    
        
    def __linear_small(self, is_death,train_data_path,basepath):
        small_dataset_file = train_data_path
        small_dataset = pandas.read_csv(small_dataset_file, encoding='UTF-8', index_col=[0])
        del small_dataset['patient_id']
        del small_dataset['name']

        # 哑变量处理
        formular = ''
        classify_attr = {'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb', 'HBeAg',
                         'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 'diuretic', 'LipidD',
                         'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access', 'ESRDcause',
                         'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease', 'bleeding',
                         'malignancy', 'ablocker', 'bblocker'}
        for column in small_dataset.columns:
            if column in classify_attr:
                formular = formular + 'C(' + column + ')+'
            else:
                formular = formular + column + '+'
        formular = formular[:-1]

        small_dataset = patsy.dmatrix(formular + '-1', small_dataset, return_type='dataframe')
        if is_death:
            T_true, E_true, T_false, E_false = ('survivaltime1', 'outcome1', 'survivaltime2', 'outcome2')
            attr_file, p632_file, var_file, kfold_file = (
                'lm_significant_attrs.txt', 'lm_stats632.csv',
                'lm_statvar.txt', 'lm_statskfold.csv'
            )
            beta_file, p_file = ('lm_coef.csv', 'lm_p.csv')
        else:
            T_true, E_true, T_false, E_false = ('survivaltime2', 'outcome2', 'survivaltime1', 'outcome1')
            attr_file, p632_file, var_file, kfold_file = (
                'lm_significant_attrs_e.txt', 'lm_stats632_e.csv',
                'lm_statvar_e.txt', 'lm_statskfold_e.csv'
            )
            beta_file, p_file = ('lm_coef_e.csv', 'lm_p_e.csv')
        del small_dataset[T_false]
        del small_dataset[E_false]

        significant_attrs = list()
        for column in small_dataset.columns:
            # print('column', column)
            if column in {T_true, E_true}:
                continue
            subset = small_dataset[[column, T_true, E_true]]
            # print('subset', subset)
            try:
                cox = CoxPHFitter()
                cox.fit(subset, T_true, E_true)
                # print('cox.summary['p'][0]:', cox.summary['p'][0])
                if cox.summary['p'][0] < 0.05:
                    significant_attrs.append(column)
            except Exception:
                continue
        output = open(attr_file, mode='w')
        for attr in significant_attrs:
            output.write(attr + '\n')
        output.close()

        input = open(attr_file)
        significant_attrs = [line.strip() for line in input.readlines()]
        input.close()

        significant_attrs.append(T_true)
        significant_attrs.append(E_true)
        print('linear_small ## sign_attr : %d' % len(significant_attrs))

        small_dataset = small_dataset[significant_attrs]

        # 10000 times .632 bootstrap
        count = 0
        stats632 = list()
        statscoef = list()
        statspvalue = list()
        while count < 10000:  # 线性训练
            try:
                train_set = small_dataset.take(numpy.random.randint(0, len(small_dataset), size=len(small_dataset)))
                test_set = small_dataset.ix[set(small_dataset.index).difference(set(train_set.index))]

                train_set.index = range(len(train_set))
                test_set.index = range(len(test_set))

                cox = CoxPHFitter()
                cox.fit(train_set, T_true, E_true)
                train_cindex = concordance_index(cox.durations, -cox.predict_partial_hazard(cox.data).values.ravel(), cox.event_observed)

                statscoef.append(cox.summary[['coef']].T)
                statspvalue.append(cox.summary[['p']].T)

                # test_set
                test_actual_T = test_set[T_true].copy()
                test_actual_E = test_set[E_true].copy()
                test_variable = test_set[test_set.columns.difference([T_true, E_true])]
                test_predictT = cox.predict_expectation(test_variable)

                # small_set
                all_actual_T = small_dataset[T_true].copy()
                all_actual_E = small_dataset[E_true].copy()
                all_variable = small_dataset[small_dataset.columns.difference([T_true, E_true])]
                all_predictT = cox.predict_expectation(all_variable)

                try:
                    test_cindex = concordance_index(test_actual_T, test_predictT, test_actual_E)
                    all_cindex = concordance_index(all_actual_T, all_predictT, all_actual_E)
                except Exception:
                    test_cindex = concordance_index(test_actual_T, test_predictT)
                    all_cindex = concordance_index(all_actual_T, all_predictT)

                stats632.append([train_cindex, test_cindex, all_cindex])
                count += 1
                print('632 -> %d' % count)
            except Exception:
                continue
        stats632_df = pandas.DataFrame(stats632, columns=['train', 'test', 'all'])
        stats632_df.to_csv(p632_file, encoding='UTF-8')

        statscoef_df = pandas.DataFrame(pandas.concat(statscoef, ignore_index=True))
        statscoef_df.to_csv(beta_file, encoding='UTF-8')
        statspvalue_df = pandas.DataFrame(pandas.concat(statspvalue, ignore_index=True))
        statspvalue_df.to_csv(p_file, encoding='UTF-8')

        # 2000 times 10-fold cross-validation、十折交叉
        count = 0
        statskfold = list()
        while count < 2000:
            try:
                cox = CoxPHFitter()
                scores = k_fold_cross_validation(cox, small_dataset, T_true, E_true, 10)
                statskfold.append(scores)
                count += 1
                print('k-fold -> %d' % count)
            except Exception:
                continue
        statskfold_df = pandas.DataFrame(statskfold)
        statskfold_df.to_csv(basepath + "/" + kfold_file, encoding='UTF-8')
        
    def __predict_single(self, is_death,train_data_path,basepath):
        big_dataset_file = train_data_path
        big_dataset = pandas.read_csv(big_dataset_file, encoding='UTF-8', index_col=[0])
        del big_dataset['patient_id']
        del big_dataset['name']
        del big_dataset['tx_id']
        # del big_dataset['tx_id.1']
        del big_dataset['tx_date']

        formular = ''
        classify_attr = {'subject', 'treat_item', 'vascular_access_type',
                         'dialysis_machine', 'anticoagulation_scope',
                         'anticoagulation', 'protamine', 'replacement_way',
                         'take_food', 'fluid_infusion', 'blood_pressure_pos',
                         'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb',
                         'HBeAg', 'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 
                         'blocker', 'blocer', 'diuretic',
                         'LipidD', 'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access',
                         'ESRDcause', 'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease',
                         'bleeding', 'malignancy'}                 

        for column in big_dataset.columns:
            # print("column", column)
            if column in classify_attr:
                formular = formular + 'C(' + column + ')+'
            else:
                formular = formular + column + '+'
       
        formular = formular[:-1].encode('utf-8')
        
        # '-1'表示不添加截取列
        big_dataset = patsy.dmatrix(formular + '-1', big_dataset, return_type='dataframe')
        if is_death:
            T_true, E_true, T_false, E_false = ('survivaltime1', 'outcome1', 'survivaltime2', 'outcome2')
            attr_file, p632_file, var_file, kfold_file = (
                'lb_significant_attrs.txt', 'lb_stats632.csv',
                'lb_statvar.txt', 'lb_statskfold.csv'
            )
            beta_file, p_file = ('lb_coef.csv', 'lb_p.csv')
        else:
            T_true, E_true, T_false, E_false = ('survivaltime2', 'outcome2', 'survivaltime1', 'outcome1')
            attr_file, p632_file, var_file, kfold_file = (
                'lb_significant_attrs_e.txt', 'lb_stats632_e.csv',
                'lb_statvar_e.txt', 'lb_statskfold_e.csv'
            )
            beta_file, p_file = ('lb_coef_e.csv', 'lb_p_e.csv')
        del big_dataset[T_false]
        del big_dataset[E_false]

        significant_attrs = list()
        # 根据报错删除部分字段
        del big_dataset['k_concentration']
        del big_dataset['SDUFR_x']
        del big_dataset['SDUFR_y']
        del big_dataset['SDUFR_y_v']
        del big_dataset['protamine_c']
        del big_dataset['k_concentration_c']
        
        """如果已经挑选出了具有统计意义的风险因子则不需要执行以下验证风险因子统计学意义的片段 """
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++
#        for column in big_dataset.columns:
#            if column in {T_true, E_true}:
#                continue
#            subset = big_dataset[[column, T_true, E_true]]
#            # print('subset', subset)
#            try:
#                # print('start fitting ')
#                cox = CoxPHFitter()
#                cox.fit(subset, T_true, E_true)
#                help(cox)
#                print('cox value:', cox.print_summary())
#                print('p value:', cox.summary['p'][0])
#                if cox.summary['p'][0] < 0.05:
#                    # print(column, cox.summary['p'][0])
#                    significant_attrs.append(column)
#            except Exception:
#                continue
#        output = open(basepath+"/"+attr_file, mode='w')
#        for attr in significant_attrs:
#            output.write(attr + '\n')
#        output.close()
        #++++++++++++++++++++++++++++++++++++++++++++++++++++
        input = open(basepath+"/"+attr_file)
        significant_attrs = [line.strip() for line in input.readlines()]
        input.close()
        significant_attrs.append(T_true)
        significant_attrs.append(E_true)
        print('linear_big ## sign_attr : %d' % len(significant_attrs))
        print(len(significant_attrs), T_true, E_true)
        
        big_dataset = big_dataset[significant_attrs]
        print(len(big_dataset.columns))
#        10000 times .632 bootstrap
        count = 9999
        stats632 = list()
        statscoef = list()
        statspvalue = list()
        while count < 10000:
            print('count', count)
            try:
                train_set = big_dataset.sample(1500, replace=False)
                test_set = big_dataset.sample(1500, replace=False)
                print('try fitting......', len(big_dataset), len(train_set), len(test_set))
                cox = CoxPHFitter()
                cox.fit(train_set, T_true, E_true)
                train_cindex = concordance_index(cox.durations, -cox.predict_partial_hazard(cox.data).values.ravel(),
                                                 cox.event_observed)

                statscoef.append(cox.summary[['coef']].T)
                statspvalue.append(cox.summary[['p']].T)

                print('try predicting......')
                # test_set
                test_actual_T = test_set[T_true]
                test_actual_E = test_set[E_true]
                test_variable = test_set[test_set.columns.difference([T_true, E_true])]
                test_predictT = cox.predict_expectation(test_variable)

                # small_set
                all_actual_T = big_dataset[T_true]
                all_actual_E = big_dataset[E_true]
                all_variable = big_dataset[big_dataset.columns.difference([T_true, E_true])]
                all_predictT = cox.predict_expectation(all_variable)

                print('try cindexing......')
                try:
                    test_cindex = concordance_index(test_actual_T, test_predictT, test_actual_E)
                    all_cindex = concordance_index(all_actual_T, all_predictT, all_actual_E)
                except Exception:
                    test_cindex = concordance_index(test_actual_T, test_predictT)
                    all_cindex = concordance_index(all_actual_T, all_predictT)

                stats632.append([train_cindex, test_cindex, all_cindex])
                count += 1
                print('632 -> %d' % count)
            except Exception as e:
                print(e.message)
                continue
        stats632_df = pandas.DataFrame(stats632, columns=['train', 'test', 'all'])
#        stats632_df.to_csv(p632_file, encoding='UTF-8')
        statscoef_df = pandas.DataFrame(pandas.concat(statscoef, ignore_index=True))
#        statscoef_df.to_csv(beta_file, encoding='UTF-8')
        statspvalue_df = pandas.DataFrame(pandas.concat(statspvalue, ignore_index=True))
#        statspvalue_df.to_csv(p_file, encoding='UTF-8')
        print('10000 times .632 bootstrap has done.')

        
    def __linear_big(self, is_death,train_data_path,basepath):
        big_dataset_file = train_data_path
        big_dataset = pandas.read_csv(big_dataset_file, encoding='UTF-8', index_col=[0])
        del big_dataset['patient_id']
        del big_dataset['name']
        del big_dataset['tx_id']
        # del big_dataset['tx_id.1']
        del big_dataset['tx_date']

        formular = ''
        # classify_attr = {'subject', 'treat_item', 'vascular_access_type',
        #                  'dialysis_machine', 'reuse_times', 'anticoagulation_scope',
        #                  'anticoagulation', 'protamine', 'replacement_way',
        #                  'take_food', 'fluid_infusion', 'blood_pressure_pos',
        #                  'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb',
        #                  'HBeAg', 'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 'diuretic',
        #                  'LipidD', 'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access',
        #                  'ESRDcause', 'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease',
        #                  'bleeding', 'malignancy', 'ablocker', 'bblocker'}
        classify_attr = {'subject', 'treat_item', 'vascular_access_type',
                         'dialysis_machine', 'anticoagulation_scope',
                         'anticoagulation', 'protamine', 'replacement_way',
                         'take_food', 'fluid_infusion', 'blood_pressure_pos',
                         'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb',
                         'HBeAg', 'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 
                         'blocker', 'blocer', 'diuretic',
                         'LipidD', 'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access',
                         'ESRDcause', 'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease',
                         'bleeding', 'malignancy'}                 
        # u'\xa6\xc2blocker'
        # print('classify_attr.dtype:', classify_attr.shape)
        

        for column in big_dataset.columns:
            # print("column", column)
            if column in classify_attr:
                formular = formular + 'C(' + column + ')+'
            else:
                formular = formular + column + '+'
        # print('formular:', formular)
        # 去掉最后面的'+'
        # type(formular): <type 'unicode'>
        formular = formular[:-1].encode('utf-8')
        # print('formular[:-1].type:', type(formular))
        
        # '-1'表示不添加截取列
        big_dataset = patsy.dmatrix(formular + '-1', big_dataset, return_type='dataframe')
        # print(type(big_dataset)) 
        # print(big_dataset.columns)
        # print('big_dataset:', big_dataset)
        if is_death:
            T_true, E_true, T_false, E_false = ('survivaltime1', 'outcome1', 'survivaltime2', 'outcome2')
            attr_file, p632_file, var_file, kfold_file = (
                'lb_significant_attrs.txt', 'lb_stats632.csv',
                'lb_statvar.txt', 'lb_statskfold.csv'
            )
            beta_file, p_file = ('lb_coef.csv', 'lb_p.csv')
        else:
            T_true, E_true, T_false, E_false = ('survivaltime2', 'outcome2', 'survivaltime1', 'outcome1')
            attr_file, p632_file, var_file, kfold_file = (
                'lb_significant_attrs_e.txt', 'lb_stats632_e.csv',
                'lb_statvar_e.txt', 'lb_statskfold_e.csv'
            )
            beta_file, p_file = ('lb_coef_e.csv', 'lb_p_e.csv')
        del big_dataset[T_false]
        del big_dataset[E_false]

        significant_attrs = list()
        # 根据报错删除部分字段
        del big_dataset['k_concentration']
        del big_dataset['SDUFR_x']
        del big_dataset['SDUFR_y']
        del big_dataset['SDUFR_y_v']
        del big_dataset['protamine_c']
        del big_dataset['k_concentration_c']
        
        """如果已经挑选出了具有统计意义的风险因子则不需要执行以下验证风险因子统计学意义的片段 """
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++
#        for column in big_dataset.columns:
#            if column in {T_true, E_true}:
#                continue
#            subset = big_dataset[[column, T_true, E_true]]
#            # print('subset', subset)
#            try:
#                # print('start fitting ')
#                cox = CoxPHFitter()
#                cox.fit(subset, T_true, E_true)
#                help(cox)
#                print('cox value:', cox.print_summary())
#                print('p value:', cox.summary['p'][0])
#                if cox.summary['p'][0] < 0.05:
#                    # print(column, cox.summary['p'][0])
#                    significant_attrs.append(column)
#            except Exception:
#                continue
#        output = open(basepath+"/"+attr_file, mode='w')
#        for attr in significant_attrs:
#            output.write(attr + '\n')
#        output.close()
        #++++++++++++++++++++++++++++++++++++++++++++++++++++
        input = open(basepath+"/"+attr_file)
        significant_attrs = [line.strip() for line in input.readlines()]
        input.close()
        significant_attrs.append(T_true)
        significant_attrs.append(E_true)
        print('linear_big ## sign_attr : %d' % len(significant_attrs))
        print(len(significant_attrs), T_true, E_true)
        
        big_dataset = big_dataset[significant_attrs]
        print(len(big_dataset.columns))
#        exit()

#        10000 times .632 bootstrap
        count = 0
        stats632 = list()
        statscoef = list()
        statspvalue = list()
        while count < 10000:
            print('count', count)
            try:
                 # big_dataset = big_dataset.take(numpy.random.permutation(len(big_dataset)))
                 # big_dataset.index = range(len(big_dataset))
                 # percent = int(len(big_dataset) * 0.30)
                 # train_set = big_dataset[:-percent]
                 # test_set = big_dataset[-percent:]
                 # train_set.index = range(len(train_set))
                 # test_set.index = range(len(test_set))

                train_set = big_dataset.sample(1500, replace=False)
                test_set = big_dataset.sample(1500, replace=False)

                print('try fitting......', len(big_dataset), len(train_set), len(test_set))
                cox = CoxPHFitter()
                cox.fit(train_set, T_true, E_true)
                train_cindex = concordance_index(cox.durations, -cox.predict_partial_hazard(cox.data).values.ravel(),
                                                 cox.event_observed)

                statscoef.append(cox.summary[['coef']].T)
                statspvalue.append(cox.summary[['p']].T)

                print('try predicting......')
                # test_set
                test_actual_T = test_set[T_true]
                test_actual_E = test_set[E_true]
                test_variable = test_set[test_set.columns.difference([T_true, E_true])]
                test_predictT = cox.predict_expectation(test_variable)

                # small_set
                all_actual_T = big_dataset[T_true]
                all_actual_E = big_dataset[E_true]
                all_variable = big_dataset[big_dataset.columns.difference([T_true, E_true])]
                all_predictT = cox.predict_expectation(all_variable)

                print('try cindexing......')
                try:
                    test_cindex = concordance_index(test_actual_T, test_predictT, test_actual_E)
                    all_cindex = concordance_index(all_actual_T, all_predictT, all_actual_E)
                except Exception:
                    test_cindex = concordance_index(test_actual_T, test_predictT)
                    all_cindex = concordance_index(all_actual_T, all_predictT)

                print(train_cindex, test_cindex, all_cindex)
                 # 0.5 0.5 0.5
                 # 0.963726363744 0.965792024703 0.964552831227
                 # 0.5 0.5 0.5
                 # 0.5 0.5 0.5
                 # 0.940458783243 0.939660104788 0.940145223899
                 # 0.950570809577 0.946854258363 0.949067405671
                 # 0.941352881629 0.941623634389 0.941462605414
                 # 0.5 0.5 0.5
                stats632.append([train_cindex, test_cindex, all_cindex])
                count += 1
                print('632 -> %d' % count)
            except Exception as e:
                print(e.message)
                continue
        stats632_df = pandas.DataFrame(stats632, columns=['train', 'test', 'all'])
        stats632_df.to_csv(p632_file, encoding='UTF-8')
        statscoef_df = pandas.DataFrame(pandas.concat(statscoef, ignore_index=True))
        statscoef_df.to_csv(beta_file, encoding='UTF-8')
        statspvalue_df = pandas.DataFrame(pandas.concat(statspvalue, ignore_index=True))
        statspvalue_df.to_csv(p_file, encoding='UTF-8')
        print('10000 times .632 bootstrap has done.')

         # 2000 times 10-fold cross-validation
#        count = 0
#        statskfold = list()
#        while count < 50:
#            try:
#                cox = CoxPHFitter()
#                print('k-folding......')
#                train_set = big_dataset
##                train_set = big_dataset.sample(6000, replace=False)
#                scores = k_fold_cross_validation(cox, train_set, T_true, E_true, 3)
#                print(scores)
#                 # [0.5, 0.5, 0.5]
#                 # [0.5, 0.5, 0.94409848057385537]
#                statskfold.append(scores)
#                count += 1
#                print('k-fold -> %d' % count)
#            except Exception as e:
#                print(e.message)
#                continue
#        statskfold_df = pandas.DataFrame(statskfold)
#        statskfold_df.to_csv(basepath+"/"+kfold_file, encoding='UTF-8')
#        print('linear big has done.')
    
    
    
    def __deep_small_train(self,is_death,train_data_path,result_single_dir,result_gather_dir):
        small_dataset_file = train_data_path
        small_dataset = pandas.read_csv(small_dataset_file, encoding='UTF-8', index_col=[0])
        del small_dataset['patient_id']
        del small_dataset['name']

        formular = ''
        classify_attr = {'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb', 'HBeAg',
                         'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 'diuretic', 'LipidD',
                         'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access', 'ESRDcause',
                         'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease', 'bleeding',
                         'malignancy', 'ablocker', 'bblocker'}
        for column in small_dataset.columns:
            if column in classify_attr:
                formular = formular + 'C(' + column + ')+'
            else:
                formular = formular + column + '+'
        formular = formular[:-1]

        small_dataset = patsy.dmatrix(formular + '-1', small_dataset, return_type='dataframe')
        if is_death:
            T_true, E_true, T_false, E_false = ('survivaltime1', 'outcome1', 'survivaltime2', 'outcome2')
            attr_file, p632_file, var_file, kfold_file = (
                'lm_significant_attrs.txt', 'lm_stats632.csv',
                'lm_statvar.txt', 'lm_statskfold.csv'
            )
        else:
            T_true, E_true, T_false, E_false = ('survivaltime2', 'outcome2', 'survivaltime1', 'outcome1')
            attr_file, p632_file, var_file, kfold_file = (
                'lm_significant_attrs_e.txt', 'lm_stats632_e.csv',
                'lm_statvar_e.txt', 'lm_statskfold_e.csv'
            )
        del small_dataset[T_false]
        del small_dataset[E_false]

        print(len(small_dataset.columns), T_true, E_true)
        for column in small_dataset.columns:
            small_dataset[column] = small_dataset[column].astype(numpy.float32)
        small_dataset[E_true] = small_dataset[E_true].astype(numpy.int32)

        var_num = len(small_dataset.columns) - 2
        all_len = len(small_dataset)
        percent = int(all_len * 0.1)

        # train_data = small_dataset.take(numpy.random.randint(0, len(small_dataset), size=len(small_dataset)))
        # valid_data = small_dataset.ix[set(small_dataset.index).difference(set(train_data.index))]
        #
        # train_data.index = range(len(train_data))
        # valid_data.index = range(len(valid_data))
        #
        # train_set = {
        #     'x': train_data[train_data.columns.difference([T_true, E_true])].values,
        #     't': train_data[T_true].values,
        #     'e': train_data[E_true].values
        # }
        # valid_set = {
        #     'x': valid_data[valid_data.columns.difference([T_true, E_true])].values,
        #     't': valid_data[T_true].values,
        #     'e': valid_data[E_true].values
        # }
        # all_set = {
        #     'x': small_dataset[small_dataset.columns.difference([T_true, E_true])].values,
        #     't': small_dataset[T_true].values,
        #     'e': small_dataset[E_true].values
        # }
        #
        # train_len = len(train_data)
        # valid_len = len(valid_data)
        # print(all_len, train_len, valid_len)

        for level in range(1, 4):  # test 1~3 level
            for unit_num in [30, 50, 100, 150, 200]:  # cell num
                hidden_layer_sizes = [unit_num for _ in range(level)]
                for learn_rate in [1e-4, 1e-5, 1e-6]:
                    hyperparams = {
                        'n_in': var_num, 'learning_rate': learn_rate, 'hidden_layers_sizes': hidden_layer_sizes
                    }
                    file_name = result_single_dir + '/result_%d_%d_%d.csv' % (level, unit_num, learn_rate * 1000000)
                    c_indexes = list()
                    for time in range(50):
                        train_data = small_dataset.take(numpy.random.randint(0, len(small_dataset), size=len(small_dataset)))
                        valid_data = small_dataset.ix[set(small_dataset.index).difference(set(train_data.index))]

                        train_data.index = range(len(train_data))
                        valid_data.index = range(len(valid_data))

                        train_set = {
                            'x': train_data[train_data.columns.difference([T_true, E_true])].values,
                            't': train_data[T_true].values,
                            'e': train_data[E_true].values
                        }
                        valid_set = {
                            'x': valid_data[valid_data.columns.difference([T_true, E_true])].values,
                            't': valid_data[T_true].values,
                            'e': valid_data[E_true].values
                        }
                        all_set = {
                            'x': small_dataset[small_dataset.columns.difference([T_true, E_true])].values,
                            't': small_dataset[T_true].values,
                            'e': small_dataset[E_true].values
                        }
                        network = DeepSurv(standardize=True, batch_norm=True, dropout=0.5, lr_decay=1.0, **hyperparams)
                        network.train(train_data=train_set, n_epochs=100, validation_frequency=1, verbose=True)
                        t_ci = network.get_concordance_index(**train_set)
                        v_ci = network.get_concordance_index(**valid_set)
                        a_ci = network.get_concordance_index(**all_set)
                        c_indexes.append([t_ci, v_ci, a_ci])
                        print(time, level, unit_num, learn_rate, t_ci, v_ci, a_ci)
                    c_indexes_df = pandas.DataFrame(c_indexes, columns=['train', 'test', 'all'])
                    c_indexes_df.to_csv(file_name, encoding='UTF-8')
                    
                    
                    
    
    """
        Deep network training
        is_death = True:death analysis;is_death = False : csd(cardiovascular) analysis
        train_data_path:the path of the training data
        result_single_path: where the result single file save
    """
    def __deep_big_train(self,is_death,train_data_path,result_single_dir,result_gather_dir):
        print("deep_big_train")
        big_dataset_file = train_data_path
        big_dataset = pandas.read_csv(big_dataset_file, encoding='UTF-8', index_col=[0])
        del big_dataset['patient_id']
        del big_dataset['name']
        del big_dataset['tx_id']
        # del big_dataset['tx_id.1']
        del big_dataset['tx_date']

        formular = ''
        # classify_attr = {'subject', 'treat_item', 'vascular_access_type',
        #                  'dialysis_machine', 'reuse_times', 'anticoagulation_scope',
        #                  'anticoagulation', 'protamine', 'replacement_way',
        #                  'take_food', 'fluid_infusion', 'blood_pressure_pos',
        #                  'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb',
        #                  'HBeAg', 'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 'diuretic',
        #                  'LipidD', 'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access',
        #                  'ESRDcause', 'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease',
        #                  'bleeding', 'malignancy', 'ablocker', 'bblocker'}
        classify_attr = {'subject', 'treat_item', 'vascular_access_type',
                         'dialysis_machine', 'anticoagulation_scope',
                         'anticoagulation', 'protamine', 'replacement_way',
                         'take_food', 'fluid_infusion', 'blood_pressure_pos',
                         'gender', 'smoking', 'highflux', 'payment', 'marital', 'alcohol', 'HBsAg', 'HBsAb',
                         'HBeAg', 'HBeAb', 'HBcAb', 'HCV', 'anticoagulant', 'EPO', 'CCB', 'ACEI', 'ARB', 
                         'blocker', 'blocer', 'diuretic',
                         'LipidD', 'CaPB', 'NCaPB', 'VitD', 'mucosaprotect', 'H2RA', 'PPI', 'APUD', 'access',
                         'ESRDcause', 'hypertension', 'DM', 'cardiovasculardisease', 'cerebrovasculardisease',
                         'bleeding', 'malignancy'}

        for column in big_dataset.columns:
            if column in classify_attr:
                formular = formular + 'C(' + column + ')+'
            else:
                formular = formular + column + '+'
        formular = formular[:-1]

        big_dataset = patsy.dmatrix(formular + '-1', big_dataset, return_type='dataframe')
        if is_death:
            T_true, E_true, T_false, E_false = ('survivaltime1', 'outcome1', 'survivaltime2', 'outcome2')
        else:
            T_true, E_true, T_false, E_false = ('survivaltime2', 'outcome2', 'survivaltime1', 'outcome1')
        del big_dataset[T_false]
        del big_dataset[E_false]

        print(len(big_dataset.columns), T_true, E_true)
        for column in big_dataset.columns:
            big_dataset[column] = big_dataset[column].astype(numpy.float32)
        big_dataset[E_true] = big_dataset[E_true].astype(numpy.int32)

        var_num = len(big_dataset.columns) - 2
        all_len = len(big_dataset)
        percent = int(all_len * 0.1)

        big_dataset = big_dataset.take(numpy.random.permutation(all_len))
        big_dataset.index = range(all_len)

        train_data, valid_data, test_data = big_dataset[:-percent], big_dataset[-percent:-percent / 2], big_dataset[-percent / 2:]
        train_len, valid_len, test_len = len(train_data), len(valid_data), len(test_data)

        train_data.index = range(train_len)
        valid_data.index = range(valid_len)
        test_data.index = range(test_len)

        valid_set = {
            'x': valid_data[valid_data.columns.difference([T_true, E_true])].values,
            't': valid_data[T_true].values,
            'e': valid_data[E_true].values
        }
        test_set = {
            'x': test_data[test_data.columns.difference([T_true, E_true])].values,
            't': test_data[T_true].values,
            'e': test_data[E_true].values
        }
        all_set = {
            'x': big_dataset[big_dataset.columns.difference([T_true, E_true])].values,
            't': big_dataset[T_true].values,
            'e': big_dataset[E_true].values
        }
        print(all_len, train_len, valid_len, test_len)
        #calculate c_indexesaverage
        train_times = 0;
        start_time = Time.time()
        # 66875 60188 3343 3344
        for level in range(1, 4):  # test 1~3 level
            # for unit_num in [8, 16, 32, 64, 128, 256, 512]:  # cell num
            for unit_num in [30, 50, 100, 150, 200]:  # cell num
                for learn_rate in [1e-4, 1e-5, 1e-6]:  # learn rate
                    hidden_layer_sizes = [unit_num for _ in range(level)]
                    hyperparams = {
                        'n_in': var_num, 'learning_rate': learn_rate, 'hidden_layers_sizes': hidden_layer_sizes
                    }
                    for batch_size in [5000, 2000, 1000, 500, 256, 100, 50, 20, 10, 5, 2, 1]:
#                    for batch_size in [500]:
                        # for batch_size in [1000, 500, 256, 100, 50, 20, 10, 5, 2, 1]:
                        """
                            standardize=True：在输入层之后加入标准化层；
                            dropout=0.5：随机使隐藏层50%的神经元停止工作，防止过拟合
                            batch_norm=True：加入批量归一化层
                            
                            hyperparams = {
                            'n_in': var_num, 输入节点数
                            'learning_rate': 1e-5,学习率
                            'hidden_layers_sizes': [100] 每个隐层的大小 
                            }
                        """
                        network = DeepSurv(standardize=True, batch_norm=True, dropout=0.5, **hyperparams)
                        help(network.train)
                        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                        help(network)
                        file_name = result_single_dir+'/result_%d_%d_%d_%d.csv' % (level, unit_num, batch_size, learn_rate * 1000000)
                        batches = int(train_len / batch_size)
                        c_indexes = list()
                        try:
                            is_convergence = False
#                            for epoch in range(batch_size):  # test two iter
                            for epoch in range(batch_size):  # test two iter
                                for batch in range(batches):  # actual all batch
                                
#                            for epoch in range(1):  # test two iter
#                                for batch in range(3):  # actual all batch
                                    startpos = batch * batch_size
                                    endpos = (batch + 1) * batch_size if (batch + 2) * batch_size <= len(train_data) else len(train_data) - 1 
                                    subset = train_data[startpos: endpos]
                                    train_set = {
                                        'x': subset[subset.columns.difference([T_true, E_true])].values,
                                        't': subset[T_true].values,
                                        'e': subset[E_true].values
                                    }
                                    """
                                        n_epochs=1:最大训练次数（所有数据训练一遍称为一个epoch）
                                        validation_frequency=1:网络计算验证的频率，减少该值可以加快训练速度
                                        verbose=True：Ture则输出额外信息到标准输出流
                                    """
                                    log = network.train(train_data=train_set, valid_data=valid_set, n_epochs=100, validation_frequency=1, verbose=False)
                                    t_ci = network.get_concordance_index(**train_set)
                                    e_ci = network.get_concordance_index(**test_set)
                                    v_ci = network.get_concordance_index(**valid_set)
                                    a_ci = network.get_concordance_index(**all_set)
                                    c_indexes.append([t_ci, e_ci,v_ci, a_ci, log['train'][0], log['valid'][0]])
                                    print(level, unit_num, learn_rate, batch_size, t_ci, e_ci,v_ci, a_ci, log['train'][0], log['valid'][0],log['process_time'])
                                    print(epoch,batch)
                                    cur_time = Time.time()
                                    self.__printTrainInfo(cur_time - start_time,train_times*100/(3*5*3*12))
                                    if (t_ci == 0.5 and e_ci == 0.5 and v_ci == 0.5 and a_ci == 0.5) or len(c_indexes) >= 600:
                                        is_convergence = True
                                        break
                                    
                                if is_convergence:
                                    break
                                
#                                subset = train_data[-batch_size:]
#                                train_set = {
#                                    'x': subset[subset.columns.difference([T_true, E_true])].values,
#                                    't': subset[T_true].values,
#                                    'e': subset[E_true].values
#                                }
#                                log = network.train(train_data=train_set, valid_data=valid_set, n_epochs=1, validation_frequency=1, verbose=False)
#                                t_ci = network.get_concordance_index(**train_set)
#                                e_ci = network.get_concordance_index(**test_set)
#                                a_ci = network.get_concordance_index(**all_set)
#                                c_indexes.append([t_ci, e_ci, a_ci, log['train'][0], log['valid'][0]])
#                                print(level, unit_num, learn_rate, batch_size, t_ci, e_ci, a_ci, log['train'][0], log['valid'][0], log['process_time'])
                        except Exception as e:
                            print(e.message)
                        finally:
                            #训练次数
                            train_times = train_times + 1
                            c_indexes_df = pandas.DataFrame(c_indexes, columns=['train', 'test', 'validate','all', 'train_loss', 'valid_loss'])
                            c_indexes_df.to_csv(file_name, encoding='UTF-8')
                            self.__writeListToFile(result_gather_dir+"/result.txt",self.__ave_index(file_name,c_indexes_df))
                        # try-except
                    # batch size
                # learn rate
            # unit number
        # level
    def __printTrainInfo(self,seconds,percent):
        c_hours = str(int(seconds)/3600)
        c_min = str(int(seconds/60)%60)
        c_seconds = str(int(seconds)%60)
        rstr = ""
        if percent == 0:
            rstr = "Remaining Train Time: Unknown"
        else:
            r_r = seconds*100/percent
            r_hours = str(int(r_r)/3600)
            r_min = str(int(r_r/60)%60)
            r_seconds = str(int(r_r)%60)
            rstr = "Estimating Remain Train Time: "+r_hours+": "+r_min+": "+r_seconds
        time_str = "Time Consume: "+c_hours+": "+c_min+": "+c_seconds+"------>"+rstr
        print("Finished Percent"+str(percent)+"%"+"-----------"+time_str)
    def __writeListToFile(self,filename,listcontents):
        fo = open(filename,'a')
        string = ""
        for item in listcontents:
            string= string +" "+ str(item)
        fo.writelines(string+"\n")
        fo.close()
    """计算均值"""
    def __ave_index(self,super_param,c_indexes_df):
        c_indexes_df = c_indexes_df.dropna(axis = 0,how = 'any')
#        train_ave,test_ave,validate_ave,all_ave,train_loss,valid_loss,test_loss,all_loss = 0,0,0,0,0,0,0,0
#        col_label = ['train','test','validate','all','train_loss','valid_loss','test_loss','all_loss']
        result_list = list()
        result_list.append(super_param)
        for col_name in c_indexes_df.columns:
            result_list.append(c_indexes_df[col_name].mean())
        result_list.append(len(c_indexes_df))
        return result_list
