# -*- coding: utf-8 -*-
from __future__ import print_function
import numpy as np
class Item:
    def __init__(self):
        print("Item")
        
    def deal_item(self, item_csv):
        print('Total lines: %d' % len(item_csv))
        for col in item_csv.columns:
            if len(item_csv[col].dropna()) != len(item_csv):
                print(('[%s]  Len: %d, NotNullLen: %d' % (col, len(item_csv[col]), len(item_csv[col].dropna()))))
        for col in item_csv.columns:
            print('column -> %s, type -> %s' % (col, item_csv[col].dtype))
        print(*list(item_csv['breathe'].astype(np.str).unique()))
        # Total lines: 18462

        item_csv['check_time'] = item_csv['check_time'].astype(np.str).str.split(' ').str.get(1)
        item_csv['check_time'] = '1900-01-01 ' + item_csv['check_time']
        # 补充
        # item_csv['check_time'] = (item_csv['check_time']- pd.to_datetime('1900-01-01')).map(lambda x: x.seconds / 3600.0)

        # [vein_pressure]  Len: 18462, NotNullLen: 13206
        print('vein_pressure', item_csv['vein_pressure'].value_counts())
        # 分为小于等于150、大于150两类，缺失看前后
        vein = item_csv['vein_pressure'].copy()
        vein[(vein.notnull()) & (vein <= 150)] = '[<=150]'
        vein[(vein.notnull()) & (vein != '[<=150]')] = '[>150]'
        item_csv['vein_pressure'] = vein

        # [membrane_pressure]  Len: 18462, NotNullLen: 13206
        print(item_csv['membrane_pressure'].value_counts())
        # 分为小于等于300、大于300两类，缺失看前后
        membrane = item_csv['membrane_pressure'].copy()
        membrane[(membrane.notnull())&(membrane <= 300)] = '[<=300]'
        membrane[(membrane.notnull())&(membrane != '[<=300]')] = '[>300]'
        item_csv['membrane_pressure'] = membrane

        # [blood_flow_volume]  Len: 18462, NotNullLen: 13212
        print(item_csv['blood_flow_volume'].value_counts())
        # 高阈值350，低阈值150，缺失看前后
        blood = item_csv['blood_flow_volume'].copy()
        blood[(blood.notnull())&(blood >= 350)] = 350
        blood[(blood.notnull())&(blood <= 150)] = 150
        item_csv['blood_flow_volume'] = blood

        # [na_concentration]  Len: 18462, NotNullLen: 13214
        print(item_csv['na_concentration'].value_counts())
        # 高阈值148，低阈值135，缺失看前后
        na = item_csv['na_concentration'].copy()
        na[(na.notnull())&(na >= 148)] = 148
        na[(na.notnull())&(na <= 135)] = 135
        item_csv['na_concentration'] = na

        # [body_temperature]  Len: 18462, NotNullLen: 5175
        print(item_csv['body_temperature'].value_counts())
        # 高阈值42，低阈值34，缺失和异常看前后
        # 正常体温36~37
        temp = item_csv['body_temperature'].copy()
        temp[(temp.notnull())&(temp >= 42)] = np.nan
        temp[(temp.notnull())&(temp <= 34)] = np.nan
        item_csv['body_temperature'] = temp

        # [SBP]  Len: 18462, NotNullLen: 18426
        print(item_csv['SBP'].value_counts())
        # 高阈值250，低阈值90，缺失和异常看前后
        sbp = item_csv['SBP'].copy()
        sbp[(sbp.notnull())&(sbp > 250)] = np.nan
        sbp[(sbp.notnull())&(sbp < 90)] = np.nan
        item_csv['SBP'] = sbp

        # [DBP]  Len: 18462, NotNullLen: 18425
        print(item_csv['DBP'].value_counts())
        # 高阈值200，低阈值40，缺失和异常看前后
        dbp = item_csv['DBP'].copy()
        dbp[(dbp.notnull())&(dbp > 200)] = np.nan
        dbp[(dbp.notnull())&(dbp < 40)] = np.nan
        item_csv['DBP'] = dbp

        # [pulse]  Len: 18462, NotNullLen: 18425
        print(item_csv['pulse'].value_counts())
        # 高阈值150，低阈值40，缺失和异常看前后
        pulse = item_csv['pulse'].copy()
        pulse[(pulse.notnull())&(pulse > 150)] = np.nan
        pulse[(pulse.notnull())&(pulse < 40)] = np.nan
        item_csv['pulse'] = pulse

        # [breathe]  Len: 528433, NotNullLen: 527088
        # [breathe]  Len: 18462, NotNullLen: 18444
        print(item_csv['breathe'].value_counts())
        # 高阈值30，低阈值8，缺失和异常看前后
        breathe = item_csv['breathe'].copy()
        breathe[(breathe.notnull()) & (breathe > 30)] = np.nan
        breathe[(breathe.notnull()) & (breathe < 8)] = np.nan
        item_csv['breathe'] = breathe

        return item_csv