# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from service.predict_service import PredictService
class PredictController:
    def __init__(self):
        print("PredictController")
        self.predict_service = PredictService()
    def predict(self):
        train_data_path = r'../../datafile/orifile/LG/dataset/p_i_r_l_combined.csv'
        basepath = r'../../datafile/resfile/LG/linear/big'
        self.predict_service.predict_individual_cds(train_data_path,basepath)
predictcontroller = PredictController()
predictcontroller.predict()