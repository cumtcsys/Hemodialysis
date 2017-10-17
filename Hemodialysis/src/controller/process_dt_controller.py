# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from service.process_dt_service import ProcessDTService
class ProcessDTController:
    def __init__(self):
        print("DTController")
        self.__process_dt_service = ProcessDTService()
        self.item_cleaned_path =  r'../../datafile/orifile/LG/cleaned/cleaned/item_cleaned.csv'
        self.patient_cleaned_path =  r'../../datafile/orifile/LG/cleaned/cleaned/patient_cleaned.csv'
        self.record_cleaned_path =  r'../../datafile/orifile/LG/cleaned/cleaned/record_cleaned.csv'
        self.record_file_return_path = r'../../datafile/orifile/LG/analysis_data/recorditem.csv'
        self.item_result_path = r'../../datafile/orifile/LG/caches/itemresult.h5'
    def clean_data(self):
        self.__process_dt_service.clean_data(self.patient_cleaned_path,self.item_cleaned_path,self.record_cleaned_path)
    def prepare_data(self):
        self.__process_dt_service.prepare_data(self.patient_cleaned_path,self.item_cleaned_path
                ,self.record_cleaned_path,self.record_file_return_path,self.item_result_path)
        
process_dt_controller = ProcessDTController()
"""clean_data() test success"""
#process_dt_controller.clean_data()
process_dt_controller.prepare_data()
