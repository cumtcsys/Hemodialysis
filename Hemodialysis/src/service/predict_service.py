# -*- coding: utf-8 -*-
import pandas as pd
import patsy
from lifelines import CoxPHFitter
from lifelines.utils import k_fold_cross_validation, concordance_index
class PredictService:
    def __init__(self):
        print("PredictService")
    def predict_individual_death(self,train_data_path,basepath):
        self.__predict_individual(True,train_data_path,basepath)
        
    def predict_individual_cds(self,train_data_path,basepath):
        self.__predict_individual(False,train_data_path,basepath)
        
    def __predict_individual(self, is_death,train_data_path,basepath):
        big_dataset_file = train_data_path
        big_dataset = pd.read_csv(big_dataset_file, encoding='UTF-8', index_col=[0])
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
        cox = CoxPHFitter()
        if count < 10000:
            print('count', count)
            try:
                train_set = big_dataset.sample(1500, replace=False)
                test_set = big_dataset.sample(1, replace=False)
                print('try fitting......', len(big_dataset), len(train_set), len(test_set))
#                cox = CoxPHFitter()
                cox = cox.fit(train_set, T_true, E_true)
                print(test_set)
                cox.predict_survival_function(test_set).plot()
                print(cox.predict_log_hazard_relative_to_mean(test_set))
#                for t_index,t_item in test_set.iterrows:
#                    print(str(t_index)+"predict_survival_function")
#                    print(cox.predict_survival_function(t_item))
#                    cox.predict_survival_function(t_item).plot()
#                    print(str(t_index)+"predict_survival_function")
#                    print(cox.predict_survival_function(t_item))
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
#                all_actual_T = big_dataset[T_true]
#                all_actual_E = big_dataset[E_true]
#                all_variable = big_dataset[big_dataset.columns.difference([T_true, E_true])]
#                all_predictT = cox.predict_expectation(all_variable)
#
#                print('try cindexing......')
                try:
                    test_cindex = concordance_index(test_actual_T, test_predictT, test_actual_E)
#                    all_cindex = concordance_index(all_actual_T, all_predictT, all_actual_E)
                except Exception:
                    test_cindex = concordance_index(test_actual_T, test_predictT)
#                    all_cindex = concordance_index(all_actual_T, all_predictT)
#
#                stats632.append([train_cindex, test_cindex, all_cindex])
                count += 1
                print('632 -> %d' % count)
                
            except Exception as e:
                print(e.message)
            
            mean_patient = self.__filter_dt(test_set)
            print(cox.predict_log_hazard_relative_to_mean(test_set))
#            mean_hazard = cox.predict_expectation(mean_patient)
            print(mean_hazard)

    def __filter_dt(self,test_set):
        mean_patient = pd.DataFrame()
#        print(test_set.columns)
        for _index,_item in test_set.iterrows():
            if _item['survivaltime2'] <= 36:
                test_set.drop([_index],axis = 0,inplace = True)
        temp = dict()        
#        for _col in test_set.columns:
#            temp[_col] = test_set[_col].mean()
        temp = test_set.mean()
#        print(temp)
        return temp
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
