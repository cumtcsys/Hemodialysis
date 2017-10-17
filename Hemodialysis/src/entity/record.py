# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from datetime import datetime
#import sys
#from statsmodels.tsa.stattools import adfuller as ADF
#from statsmodels.stats.diagnostic import acorr_ljungbox
#from statsmodels.tsa.arima_model import ARIMA
#import deepsurv
class Record:
    def __init__(self):
        print("Record")
    def deal_record(self, record_csv):
        print('Total lines: %d' % len(record_csv))
        # 如果统一分析09年之后的单子，那么就会丧失5000多条记录
        # 反正也会分析到15年以后的记录，都不截取
        # print(len(records[records['tx_date'] >= pd.to_datetime('2009-01-01')]))  # 75042
        for col in record_csv.columns:
            # if len(record_csv[col].dropna()) != len(record_csv):
            #     print(('[%s]  Len: %d, NotNullLen: %d' % (col, len(record_csv[col]), len(record_csv[col].dropna()))), *list(record_csv[col].unique()))
            if len(record_csv[col].dropna()) != len(record_csv):
                print(('[%s]  Len: %d, NotNullLen: %d' % (col, len(record_csv[col]), len(record_csv[col].dropna()))))
        # Total lines: 80344

        # [tx_date]  Len: 80344, NotNullLen: 80334
        # (需要重采样)
        # 扔掉这十个缺失的
        records = record_csv[record_csv['tx_date'].notnull()]

        # [subject]  Len: 80344, NotNullLen: 79898
        print(records['subject'].value_counts())
        records['subject'].value_counts().plot(kind='bar')
        plt.show()
        # 通过人工整理即可（计算比例将小部分归为其他，避免哑变量过多）
        # 分为人工肾和非人工肾，缺失默认为非人工肾（这里错了，是人工肾，暂时不改）
        # 人工肾1，非人工肾0
        subject = records['subject'].copy()
        subject[records['subject'] == u'人工肾'] = '1'
        subject[subject.str.contains(u'人工肾').fillna(False)] = '1'
        subject[subject != '1'] = '0'
        records['subject'] = subject

        # [treat_item]  Len: 80344, NotNullLen: 80340
        print(records['treat_item'].value_counts())
        records['treat_item'].value_counts().plot(kind='bar')
        plt.show()
        # 分为血液透析0、血液透析滤过1、高通量透析2、灌流+透析3，缺失为血液透析
        treat_item = records['treat_item'].copy()
        treat_item[treat_item == u'血液透析'] = '0'
        treat_item[treat_item == u'血液透析滤过'] = '1'
        treat_item[treat_item == u'高通量透析'] = '2'
        treat_item[treat_item == u'灌流+透析'] = '3'
        treat_item[(treat_item != '0') & (treat_item != '1') & (treat_item != '2') & (treat_item != '3')] = '0'
        records['treat_item'] = treat_item

        # [vascular_access_type]  Len: 80344, NotNullLen: 80178
        print(records['vascular_access_type'].value_counts())
        # 分为中心静脉长期导管LCVC、中心静脉临时导管SCVC、自体动静脉内瘘AVF、人工血管动静脉内瘘AVG、直接穿刺puncture
        # 缺失值前向插值或者后向插值
        vascular = records['vascular_access_type'].copy()
        vascular[vascular == u'内瘘'] = 'AVF'
        vascular[vascular == u'颈内静脉插管'] = 'SCVC'
        vascular[vascular == u'人造血管'] = 'AVG'
        vascular[vascular == u'颈内静脉长期导管'] = 'LCVC'
        vascular[vascular == u'直穿'] = 'puncture'
        vascular[vascular == u'股静脉插管'] = 'SCVC'
        vascular[vascular == u'颈内静脉插管+内瘘'] = 'AVF'
        vascular[vascular == u'人造内瘘'] = 'AVF'
        vascular[vascular == u'桡动脉'] = 'puncture'
        vascular[vascular == u'颈内静脉'] = 'SCVC'
        vascular[vascular == u'锁骨下静脉插管'] = 'SCVC'
        vascular[vascular == u'内瘘+插管'] = 'AVF'
        vascular[vascular == u'静静脉'] = 'SCVC'
        vascular[vascular == u'直接穿刺'] = 'puncture'
        vascular[vascular == u'右锁骨下静脉插管'] = 'SCVC'
        vascular[vascular == u'颈内静脉插管＋内瘘'] = 'AVF'
        vascular[vascular == u'颈内静脉＋股静脉插管'] = 'SCVC'
        vascular[vascular == u'颈内静脉长期导管+直穿'] = 'LCVC'
        vascular[vascular == u'静脉+内瘘'] = 'AVF'
        vascular[vascular == u'股静脉插管+内瘘'] = 'AVF'
        vascular[vascular == u'内瘘+颈内静脉插管'] = 'AVF'
        vascular[vascular == u'股静脉插管+人造内瘘'] = 'AVF'
        vascular[vascular == u'颈内静脉插管+人造血管'] = 'AVG'
        vascular[vascular == u'股静脉插管+右侧前臂内瘘'] = 'AVF'
        vascular[vascular == u'股静脉插管+左侧前臂内瘘'] = 'AVF'
        vascular[vascular == u'颈内静脉＋股静脉置管'] = 'SCVC'
        vascular[vascular == u'颈内静脉插管内瘘'] = 'AVF'
        vascular[vascular == u'股静脉插管+人造血管'] = 'AVG'
        vascular[vascular == u'内瘘+直穿'] = 'AVF'
        vascular[vascular == u'自身静脉+人造血管'] = 'AVG'
        vascular[vascular == u'颈内静脉长期导管+内瘘'] = 'AVF'
        vascular[vascular == u'锁骨下静脉插管+静脉'] = 'SCVC'
        vascular[vascular == u'手臂静脉'] = 'SCVC'
        vascular[vascular == u'颈内静脉插管+动静脉内瘘'] = 'AVF'
        vascular[vascular == u'内瘘＋颈内静脉'] = 'AVF'
        vascular[vascular == u'股静脉插管＋AV内瘘'] = 'AVF'
        vascular[(vascular != 'AVG') & (vascular != 'AVF') & (vascular != 'puncture') & (vascular != 'LCVC') & (vascular != 'SCVC')] = np.nan
        records['vascular_access_type'] = vascular

        # [dialysis_machine]  Len: 80344, NotNullLen: 80317
        # 分为费森尤斯FSYS、金宝JB、贝朗BL、天兰TL、百特BT
        print(records['dialysis_machine'].value_counts())
        d_machine = records['dialysis_machine'].copy()
        d_machine[d_machine.str.contains(u'费森尤斯').fillna(False)] = 'FSYS'
        d_machine[d_machine.str.contains(u'金宝').fillna(False)] = 'JB'
        d_machine[d_machine.str.contains(u'贝朗').fillna(False)] = 'BL'
        d_machine[d_machine.str.contains(u'天兰').fillna(False)] = 'TL'
        d_machine[d_machine.str.contains(u'百特').fillna(False)] = 'BT'
        d_machine[(d_machine != 'FSYS') & (d_machine != 'JB') & (d_machine != 'BL') & (d_machine != 'TL') & (d_machine != 'BT')] = np.nan
        records['dialysis_machine'] = d_machine

        # [clean_machine]  Len: 80344, NotNullLen: 80307
        print(records['clean_machine'].value_counts())
        v_c = records['clean_machine'].value_counts()
        for i in v_c.index:
            print(i, v_c[i])
        # 分为小于等于1.5、大于1.5，缺失看前后
        c_map = {
            '17L': '1.7', '14L': '1.4', 'CA150': '1.5', 'F6': '1.3', 'F7': '1.6', '140H': '1.4', '6LR': '1.4',
            'F60S': '1.3', '21L': '2.1', 'BLS814SD': '1.4', 'APS650': '1.3', 'B3-1.6A': '1.6', 'TS-1.6U': '1.6',
            '17L+HA130': '1.7', '17L+130': '1.7', 'FX60': '1.3', 'F8': '1.8', 'F6+HA130': '1.3', '17': '1.7', 'TS-1.6UL': '1.6',
            'F7+130': '1.6', '14L+HA130': '1.4', 'AV600S': np.nan, 'AM-BLO-750': '1.5', '17L＋HA130': '1.7',
            'AM750': '1.5', 'Fx60': '1.3', 'TS1.6UL': '1.6', '21': '2.1', '14H': '1.4', '14L＋HA130': '1.4', 'F7+HA130': '1.6',
            'F6+130': '1.3', 'CA150(2)': '1.5', 'AM－BLO－750': '1.5', 'BLO-750': '1.5', 'LR': '1.4', '6': '1.4',
            'TS-1.6': '1.6', 'F6＋HA130': '1.3', '14OH': '1.4', 'TS-1.6ul': '1.6', 'Primus': '1.3', '21l': '2.1',
            '14L+A130': '1.4', 'TS1.6': '1.6', '17L+130H': '1.7', 'AM-750': '1.5', '17L+A130': '1.7', '2': '2.1',
            '20L': '2.0', 'primus': '1.3', 'FX': '1.3', '14L＋HA330': '1.4', '121L': '2.1', 'HA130+F6': '1.3', 'fx60': '1.3',
            '750WET': '1.5', '17L＋130': '1.7', 'ts-1.6': '1.6', 'ST-1.6UL': '1.6', '14L+HP130': '1.4', 'TS-1.6VL': '1.6',
            'F6+HP': '1.3', '17+HA130': '1.7', 'BLS814SD+F6': '1.3', 'ts-1.6ul': '1.6', 'HA330': np.nan, 'F7＋HA1330': '1.6',
            '17L＋HP': '1.7', '.F60S': '1.3', '.17L': '1.7', 'APS-60': '1.3', '14l': '1.4', 'TS1.6-UL': '1.6', 'FSL6U': '1.6',
            '14L+17L': '1.4', '17L＋130H': '1.7', 'Ts-1.6u': '1.6', '17L+17L': '1.7', '14L+130HA': '1.4', 'AM-BL0-750': '1.5',
            'FS60': '1.3', '17L+HA330': '1.7', '140H+F6': '1.4', 'HA130+17L': '1.7', '3': '1.6', 'pus2u': '1.3', '2F60S': '1.3',
            'Kf-m15': '1.5', '14L+130': '1.4', 'AMB': '1.5', '17L+HA133': '1.7', 'TS': '1.6', '17L+HP': '1.7', '+': '1.5'
        }
        c_machine = records['clean_machine'].copy()
        c_machine = c_machine.map(c_map)
        c_machine = c_machine.astype(np.float)
        c_machine[(c_machine.notnull()) & (c_machine > 1.5)] = '[>1.5]'
        c_machine[(c_machine.notnull()) & (c_machine <= 1.5)] = '[<=1.5]'
        records['clean_machine'] = c_machine

        # reuse_times为空，故舍去
        # [reuse_times]  Len: 80344, NotNullLen: 77737
        # print(records['reuse_times'].value_counts())
        # # 分为有1、无0，缺失使用前向填充或者后向填充
        # reuse = records['reuse_times'].copy()
        # reuse = reuse.astype(np.str)
        # reuse[records['reuse_times'] == 0] = '0'
        # reuse[(records['reuse_times'].notnull()) & (records['reuse_times'] != 0)] = '1'
        # records['reuse_times'] = reuse
        # print('reuse_times:')

        # [anticoagulation_scope]  Len: 80344, NotNullLen: 80306
        print(records['anticoagulation_scope'].value_counts())
        # 分为有1、无0，缺失值按有处理
        a_scope = records['anticoagulation_scope'].copy()
        a_scope[a_scope == u'全身'] = '1'
        a_scope.fillna('1', inplace=True)
        a_scope[a_scope != '1'] = '0'
        records['anticoagulation_scope'] = a_scope

        # [anticoagulation]  Len: 80344, NotNullLen: 79939
        print(records['anticoagulation'].value_counts())
        # 分为无肝素0、肝素1、低分子量肝素2
        # 0.*小额数字是低分量，大数字是肝素，克赛、速碧林、法安明是低分量，缺失值按照前向填充或者后向填充处理
        anticoagulation = records['anticoagulation'].copy()
        a_map = {
            u'克赛': '2',
            u'速碧林': '2',
            u'肝素': '1',
            u'法安明': '2',
            u'0': '0',
            u'天道': '2',
            u'无': '0',
            u'低分子': '2',
            u'3': '1',
            u'0.4ml': '2',
            u'无肝素': '0',
            u'46': '1',
            u'16': '1',
            u'0.1ml': '2',
            u'0.05 ': '2'
        }
        anticoagulation = anticoagulation.map(a_map)
        records['anticoagulation'] = anticoagulation

        # [protamine]  Len: 80344, NotNullLen: 62803
        print(records['protamine'].value_counts())
        # 分为有1、无0，默认无
        protamine = records['protamine'].copy()
        protamine[protamine == 0] = '0'
        protamine.fillna('0', inplace=True)
        protamine[protamine != '0'] = '1'
        records['protamine'] = protamine

        # [target_treat_time]  Len: 80344, NotNullLen: 80342
        print('target_treat_time:', records['target_treat_time'].value_counts())
        t_time = records['target_treat_time'].copy()
        t_time[t_time > pd.datetime(1900, 1, 1, 4)] = pd.datetime(1900, 1, 1, 4)
        records['target_treat_time'] = t_time
        print('target_treat_time change:', records['target_treat_time'].value_counts())

        # [actual_treat_time]  Len: 80344, NotNullLen: 80311
        print('actual_treat_time:', records['actual_treat_time'].value_counts())
        a_time = records['actual_treat_time'].copy()
        a_time[a_time > pd.datetime(1900, 1, 1, 6)] = pd.datetime(1900, 1, 1, 6)
        records['actual_treat_time'] = a_time
        print('actual_treat_time change:', records['target_treat_time'].value_counts())

        # [replace_amount]  Len: 80344, NotNullLen: 69862
        print(records['replace_amount'].value_counts())
        # 有大于零的数字说明有置换

        # [replacement_way]  Len: 80344, NotNullLen: 68475
        print(records['replacement_way'].value_counts())
        # 分为有1、无0，缺失是无

        r_amount = records['replace_amount'].copy()
        r_amount.fillna(0, inplace=True)
        records['replace_amount'] = r_amount
        r_way = records['replacement_way'].copy()
        r_way[r_amount == 0] = '0'
        r_way[r_way == u'无'] = '0'
        r_way[r_way != '0'] = '1'
        records['replacement_way'] = r_way

        # [ca_concentration]  Len: 80344, NotNullLen: 80212
        print(records['ca_concentration'].value_counts())
        # 分为1.25、1.5、1.75，默认1.5
        ca_map = {
            '1.25 mmol/L': '[1.25]',
            '1.5 mmol/L': '[1.5]',
            '1.25mmol/l': '[1.25]',
            '1.25': '[1.25]',
            '1.5mmol/l': '[1.5]',
            '1.75 mmol/L': '[1.75]',
            '1.5': '[1.5]'
        }
        ca = records['ca_concentration'].copy()
        ca = ca.map(ca_map)
        ca[(ca != '[1.25]')&(ca != '[1.5]')&(ca != '[1.75]')] = '[1.5]'
        records['ca_concentration'] = ca

        # [k_concentration]  Len: 80344, NotNullLen: 80161
        print(records['k_concentration'].value_counts())
        # 分为2.0和大于等于3，默认2.0
        k_map = {
            '2.0 mmol/L': '[2.0]',
            '4.0 mmol/L': '[>=3.0]',
            '3.0 mmol/L': '[>=3.0]',
            '2.0': '[2.0]',
            '4.0mmol': '[>=3.0]',
            '5.0 mmol/L': '[>=3.0]',
            '3.5 mmol/L': '[>=3.0]'
        }
        k = records['k_concentration'].copy()
        k = k.map(k_map)
        k[(k != '[2.0]')&(k != '[>=3.0]')] = '[2.0]'
        records['k_concentration'] = k

        # [dry_weight]  Len: 80344, NotNullLen: 79446
        print(records['dry_weight'].value_counts())
        # 高阈值是100，低阈值是30，缺失看年度数据
        d_weight = records['dry_weight'].copy()
        d_weight[(d_weight > 100)|(d_weight < 30)] = np.nan
        records['dry_weight'] = d_weight

        # [pre_weight]  Len: 80344, NotNullLen: 80227
        print(records['pre_weight'].value_counts())
        # 高阈值是100，低阈值是30，缺失看年度数据
        pre_weight = records['pre_weight'].copy()
        pre_weight[(pre_weight > 100)|(pre_weight < 30)] = np.nan
        records['pre_weight'] = pre_weight

        # [target_ultrafiltration]  Len: 80344, NotNullLen: 80341
        print(records['target_ultrafiltration'].value_counts())
        # 高阈值6，超过6的是异常数据，都修正为6，缺失看前后
        t_ul = records['target_ultrafiltration'].copy()
        t_ul[t_ul > 6] = 6
        records['target_ultrafiltration'] = t_ul

        # [take_food]  Len: 80344, NotNullLen: 76973
        print(records['take_food'].value_counts())
        # 分为有1、无0，默认无
        take_food = records['take_food'].copy()
        take_food[take_food < 1] = '0'
        take_food.fillna('0', inplace=True)
        take_food[take_food != '0'] = '1'
        records['take_food'] = take_food

        # [fluid_infusion]  Len: 80344, NotNullLen: 75220
        print(records['fluid_infusion'].value_counts())
        records['fluid_infusion'].value_counts().plot(kind='bar')
        plt.show()
        # 分为有1、无0
        # 100以上算有，否则算无（包括缺失数据）
        fluid = records['fluid_infusion'].copy()
        fluid[fluid >= 100] = '1'
        fluid[fluid != '1'] = '0'
        records['fluid_infusion'] = fluid

        # [after_weight]  Len: 80344, NotNullLen: 80231
        print(records['after_weight'].value_counts())
        records['after_weight'].value_counts().plot(kind='bar')
        plt.show()
        # 高阈值是100，低阈值是30，缺失看年度数据，或者考虑使用干体重代替
        after_weight = records['after_weight'].copy()
        after_weight[(after_weight > 100)|(after_weight < 30)] = np.nan
        records['after_weight'] = after_weight

        # [actual_ultrafiltration]  Len: 80344, NotNullLen: 80328
        print(records['actual_ultrafiltration'].value_counts())
        records['actual_ultrafiltration'].value_counts().plot(kind='bar')
        plt.show()
        # 高阈值6，超过6的是异常数据，都修正为6，缺失看前后
        a_ul = records['actual_ultrafiltration'].copy()
        a_ul[a_ul > 6] = 6
        records['actual_ultrafiltration'] = a_ul

        # [blood_pressure_pos]  Len: 80344, NotNullLen: 80336
        print(records['blood_pressure_pos'].value_counts())
        records['blood_pressure_pos'].value_counts().plot(kind='bar')
        plt.show()
        # 分为上肢0、下肢1，默认上肢
        b_pos = records['blood_pressure_pos'].copy()
        b_pos[b_pos == u'下肢'] = '1'
        b_pos[b_pos != '1'] = '0'
        records['blood_pressure_pos'] = b_pos
        
        # 删除reuse_times
        del records['reuse_times']

        # 以一个病人为单位分析    
        patient_file = r'cleaned/cleaned/patient.csv'
        # patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0],
        #                        parse_dates=['begin_date', 'end_date', 'center_begin_date', 'tx_begin_date', 'eventdate',
        #                                     'vascular_access_build_date', 'birth', 'dateSt', 'dateEn', 'deathdate', 'dateHD'])
        
        patients =  pd.read_csv(patient_file, encoding='UTF-8', index_col=[0])
        patients = patients[['patient_id', 'name']]
        merged = pd.merge(left=patients, right=records, on='patient_id')
        groupbypid = merged.groupby('patient_id')
        for index, cutted in groupbypid:
            print(index)
            print(cutted)
            break
        # print(merged[merged['patient_id'] == 405].sort_values(by=['tx_date'], ascending=False))

        # record.csv：透析记录的属性采用先前向填充，再后向填充的方法
        # 这里对于每个病人，将记录按日期排序之后，进行前向填充和后向填充
        # patient_ids = set(records['patient_id'])
        # for id in patient_ids:
        #     records[records['patient_id'] == id] = \
        #         records[records['patient_id'] == id].sort_values(by=['tx_date'], ascending=True).fillna(method='ffill').fillna(method='bfill')
        # return records
        # why raise SettingWithCopyWarning? but do not raise except.
        print('start ffill & bfill...')
        patient_ids = set(records['patient_id'])
        try:
            for id in patient_ids:
                records.loc[records['patient_id'] == id] = \
                    records.loc[records['patient_id'] == id].sort_values(by=['tx_date'], ascending=True).fillna(method='ffill').fillna(method='bfill')
        except:
            # 发出警告，没有抛出异常，为什么？
            print('ffill & bfill have failed')
        return records