# -*- coding: utf-8 -*-
import pandas as pd
class VisualService:
    def __init__(self):
        print("VisualService")

    def show_data(self,item_path,patient_path,record_path):
        # show item
#        item_file = r'cleaned/cleaned/item.csv'
        item_file = item_path
        items = pd.read_csv(item_file, encoding='UTF-8', index_col=[0], parse_dates=['check_time'])
        print('Total lines: %d' % len(items))
        for col in items.columns:
            if len(items[col].dropna()) != len(items):
                print(('[%s]  Len: %d, NotNullLen: %d' % (col, len(items[col]), len(items[col].dropna()))))
        for col in items.columns:
            print('column -> %s, type -> %s' % (col, items[col].dtype))
        # Total lines: 15296
        # [vein_pressure]  Len: 15296, NotNullLen: 10948
        # [membrane_pressure]  Len: 15296, NotNullLen: 10948
        # [blood_flow_volume]  Len: 15296, NotNullLen: 10954
        # [na_concentration]  Len: 15296, NotNullLen: 10956
        # [body_temperature]  Len: 15296, NotNullLen: 4290
        # [SBP]  Len: 15296, NotNullLen: 15196
        # [DBP]  Len: 15296, NotNullLen: 15250
        # [pulse]  Len: 15296, NotNullLen: 15264
        # [breathe]  Len: 15296, NotNullLen: 15280

        # show patient
        # # Len: 17, NotNullLen: 0  
        
        
#        patient_file = r'cleaned/cleaned/patient.csv'
        patient_file = patient_path
        patients =  pd.read_csv(patient_file, encoding='UTF-8', index_col=[0])
        print('Total lines: %d' % len(patients))
        for col in patients.columns:
            if len(patients[col].dropna()) != len(patients):
                print(('[%s]  Len: %d, NotNullLen: %d' % (col, len(patients[col]), len(patients[col].dropna()))))
        for col in patients.columns:
            print('column -> %s, type -> %s' % (col, patients[col].dtype))


        # show record
        # # Len: 2150, NotNullLen: 0  
        #        record_file = r'cleaned/cleaned/record.csv'
        record_file = record_path
        records = pd.read_csv(record_file, encoding='UTF-8', low_memory=False, index_col=[0],
                              parse_dates=['tx_date', 'target_treat_time', 'actual_treat_time'])
        print('Total lines: %d' % len(records))
        for col in records.columns:
            if len(records[col].dropna()) != len(records):
                print(('[%s]  Len: %d, NotNullLen: %d' % (col, len(records[col]), len(records[col].dropna()))))
        for col in records.columns:
            print('column -> %s, type -> %s' % (col, records[col].dtype))
   