# -*- coding: utf-8 -*-
class TrainViewer:
    def __init__(self):
        print("TrainViewer")
        self.__deep_big_train_data_path = r'../../datafile/orifile/LG/dataset/p_i_r_l_combined.csv'
        self.__deep_big_result_single_dir = r'../../datafile/resfile/LG/deep/big'
        self.__deep_big_result_gather_dir = r'../../datafile/resfile/LG/deep/big'
        
        self.__linear_big_train_data_path = r'../../datafile/orifile/LG/dataset/p_i_r_l_combined.csv'
        self.__linear_big_train_basepath = r'../../datafile/resfile/LG/linear/big'
        
        self.__deep_small_train_data_path = r'../../datafile/orifile/LG/dataset/dataset1.csv'
        self.__deep_small_result_single_dir = r'../../datafile/resfile/LG/deep/small'
        self.__deep_small_result_gather_dir = r'../../datafile/resfile/LG/deep/small'
        
        self.__linear_small_train_data_path = r'../../datafile/orifile/LG/dataset/dataset1.csv'
        self.__linear_small_train_basepath = r'../../datafile/resfile/LG/linear/small'
        
        
    def get_deep_big_train_data_path(self):
        return self.__deep_big_train_data_path
    def get_deep_big_result_single_dir(self):
        return self.__deep_big_result_single_dir
    def get_deep_big_result_gather_dir(self):
        return self.__deep_big_result_gather_dir
    def get_deep_small_train_data_path(self):
        return self.__deep_small_train_data_path
    def get_deep_small_result_single_dir(self):
        return self.__deep_small_result_single_dir
    def get_deep_small_result_gather_dir(self):
        return self.__deep_small_result_gather_dir
    
    """Linear start"""
    def get_linear_big_train_data_path(self):
        return self.__linear_big_train_data_path
    def get_linear_big_train_basepath(self):
        return self.__linear_big_train_basepath
    def get_linear_small_train_data_path(self):
        return self.__linear_small_train_data_path
    def get_linear_small_train_basepath(self):
        return self.__linear_small_train_basepath

