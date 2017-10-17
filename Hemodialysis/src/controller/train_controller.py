# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from service.train_service import TrainService
from viewer.train_viewer import TrainViewer
class TrainController:
    def __init__(self):
        print("TrainController")
        self.__trainservice = TrainService()
        self.__train_viewer = TrainViewer()
    def deep_big_train_cds(self):
        self.__trainservice.deep_big_train_cds(self.__train_viewer.get_deep_big_train_data_path()
                ,self.__train_viewer.get_deep_big_result_single_dir(),self.__train_viewer.get_deep_big_result_gather_dir())
    def deep_big_train_death(self):
        self.__trainservice.deep_big_train_death(self.__train_viewer.get_deep_big_train_data_path()
                ,self.__train_viewer.get_deep_big_result_single_dir(),self.__train_viewer.get_deep_big_result_gather_dir())
    def linear_big_train_cds(self):
        self.__trainservice.linear_big_train_cds(self.__train_viewer.get_linear_big_train_data_path()
                ,self.__train_viewer.get_linear_big_train_basepath())
    def linear_big_train_death(self):
        self.__trainservice.linear_big_train_death(self.__train_viewer.get_linear_big_train_data_path()
                ,self.__train_viewer.get_linear_big_train_basepath())
        
        
    """small start"""
    def deep_small_train_cds(self):
        self.__trainservice.deep_small_train_cds(self.__train_viewer.get_deep_small_train_data_path()
                ,self.__train_viewer.get_deep_small_result_single_dir(),self.__train_viewer.get_deep_small_result_gather_dir())
    def deep_small_train_death(self):
        self.__trainservice.deep_small_train_death(self.__train_viewer.get_deep_small_train_data_path()
                ,self.__train_viewer.get_deep_small_result_single_dir(),self.__train_viewer.get_deep_small_result_gather_dir())
    def linear_small_train_cds(self):
        self.__trainservice.linear_small_train_cds(self.__train_viewer.get_linear_small_train_data_path()
                ,self.__train_viewer.get_linear_small_train_basepath())
    def linear_small_train_death(self):
        self.__trainservice.linear_small_train_death(self.__train_viewer.get_linear_small_train_data_path()
                ,self.__train_viewer.get_linear_small_train_basepath())
        
train_controller = TrainController()
"""deep_big_train_cds() test success"""
#train_controller.deep_big_train_cds()
"""deep_big_train_death() test success"""
#train_controller.deep_big_train_death()
"""linear_big_train_death() test success"""
train_controller.linear_big_train_cds()
"""linear_big_train_death() test success"""
#train_controller.linear_big_train_death()
"""deep_small_train_cds() test success"""
#train_controller.deep_small_train_cds()
"""deep_small_train_death() test success"""
#train_controller.deep_small_train_death()

"""linear_small_train_cds() compile ok but has RuntimeWarning"""
#train_controller.linear_small_train_cds()
"""linear_small_train_death() compile ok but has RuntimeWarning"""
#train_controller.linear_small_train_death()