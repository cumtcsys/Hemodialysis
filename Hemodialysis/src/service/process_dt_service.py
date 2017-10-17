# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
from entity.item import Item
from entity.patient import Patient
from entity.record import Record
import pandas as pd
import numpy as np
class ProcessDTService:
    def __init__(self):
        print("ProcessDTService")
        self.patient_entity = Patient()
        self.item_entity = Item()
        self.record_entity = Record()
    def __load_data(self):  # 数据怎么来的，要看第一个版本的预处理
        self.item = pd.read_csv(r'../../datafile/orifile/LG/dirty_dataset/item.csv', parse_dates=True, encoding='UTF-8')
        self.patient = pd.read_csv(r'../../datafile/orifile/LG/dirty_dataset/patient.csv', parse_dates=True, encoding='UTF-8')
        self.record = pd.read_csv(r'../../datafile/orifile/LG/dirty_dataset/record.csv', parse_dates=True, encoding='UTF-8', low_memory=False)
        self.excel = pd.read_excel(r'../../datafile/orifile/LG/dirty_dataset/LGalldata.xls', sheetname='LGallbaseline', index_col=[0], encoding='UTF-8')
    def has_data(self):
        # 如果四个csv文件不存在，则返回False
        return not (self.item.empty & self.patient.empty & self.record.empty & self.excel.empty)    
    # 数据规约
    # 在python2里面，u表示unicode string，类型是unicode, 没有u表示byte string，类型是str。
    # 在python3里面，所有字符串都是unicode string, u前缀没有特殊含义了
    def clean_data(self,patient_cleaned_path,item_cleaned_path,record_cleaned_path):
        self.__load_data()
        self.__cut_data_amount_and_attrs(patient_cleaned_path,item_cleaned_path,record_cleaned_path)
    
    def prepare_data(self,patient_cleaned_path,item_cleaned_path,record_cleaned_path,record_file_return_path,item_result_path):
        self.clean_data(patient_cleaned_path,item_cleaned_path,record_cleaned_path)
        self.__missing_abnormal(patient_cleaned_path,item_cleaned_path,record_cleaned_path)           # 缺失和异常处理
#        self.__balance_data(patient_cleaned_path,item_cleaned_path,record_cleaned_path)                # 自定义处理，主要是避免分析时出错
        # dp.show_data()
#        self.__merge_and_fill_item(patient_cleaned_path,item_cleaned_path,record_cleaned_path) 
#        self.__item_stats(patient_cleaned_path,item_cleaned_path,record_cleaned_path,record_file_return_path,item_result_path)         
    
    def __missing_abnormal(self,patient_clean_path,item_clean_path,record_clean_path):
        # 处理病人的基本入院信息数据（缺失和异常）
        # parse_dates=['begin_date', 'end_date',...]：解析'begin_date', 'end_date'等列的值作为独立的日期列
        # patient_file = r'cleaned/cleaned/patient.csv'
        # # patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0],
        # #                        parse_dates=['begin_date', 'end_date', 'center_begin_date', 'tx_begin_date', 'eventdate',
        # #                                     'vascular_access_build_date', 'birth', 'dateSt', 'dateEn', 'deathdate', 'dateHD'])
        # index_col=[0] 使用Frame中第0列作为行标，index_col=False 在Frame中添加首列行标
        
        patient_file = patient_clean_path 
#        patient_file = r'cleaned/cleaned/patient.csv'
        
        
        patients =  pd.read_csv(patient_file, encoding='UTF-8', index_col=[0], parse_dates=['birth', 'dateSt'])
        self.patient_entity.deal_patient(patients).to_csv(patient_file, encoding='UTF-8')
        print('patient has done!')

        # 处理病人的透析记录信息数据（缺失和异常）
        record_file = record_clean_path
#        record_file = r'cleaned/cleaned/record.csv'
        
        
        records = pd.read_csv(record_file, encoding='UTF-8', low_memory=False, index_col=[0],
                               parse_dates=['tx_date', 'target_treat_time', 'actual_treat_time'])
        self.record_entity.deal_record(records).to_csv(record_file, encoding='UTF-8')
        print('records has done!')

#         处理病人的透析记录子项信息数据（缺失和异常）
        item_file = item_clean_path
#        item_file = r'cleaned/cleaned/item.csv'
        
        
        items = pd.read_csv(item_file, encoding='UTF-8', index_col=[0], parse_dates=['check_time'])
        self.item_entity.deal_item(items).to_csv(item_file, encoding='UTF-8')
        print('item has done!')
        
    def __cut_data_amount_and_attrs(self,patient_cleaned_path,item_cleaned_path,record_cleaned_path):
        if not self.has_data():
            raise ValueError(u'没有数据')
        print(self.has_data())
        # 集合所有资料齐全的病人，以excel为准，保留一份基础数据即可
        # self.patient['name'] = self.patient['name'].str.strip()  # 去空
        self.excel['name'] = self.excel['name'].str.strip()      # 去空
        # # 重复的属性保留一份即可
        # del self.patient['name']        # 名字保留一份（删掉csv的，保留Excel的）
        # del self.patient['gender']      # 性别保留一份（删掉csv的，保留Excel的）
        # del self.patient['birth_date']  # 生日保留一份（删掉csv的，保留Excel的）
        # del self.patient['nation']      # 民族为空，删除
        # del self.patient['pay_way']     # 付款方式保留一份（删掉csv的，保留Excel的）
        # del self.patient['marriage']    # 婚姻保留一份（删掉csv的，保留Excel的）
        # # 医生建议的删除属性（因为这些跟分析无关，或者大量缺失，或者毫无帮助）
        # del self.patient['blood_type']    # 血型
        # del self.patient['social_no']     # 身份证号
        # del self.patient['country']       # 国籍
        # del self.patient['birth_place']   # 出生地
        # del self.patient['admiss_times']  # ???
        # del self.patient['end_status']    # ???
        # del self.patient['x_ray_code']    # X射线号
        # del self.patient['occupation']    # 职业
        # del self.patient['home_tel']      # 户口电话
        # del self.patient['home_addr']     # 户口地址
        # del self.patient['mobile']        # 移动电话
        # del self.patient['work_addr']     # 单位地址
        # del self.patient['work_tel']      # 单位电话
        # del self.patient['work_zipcode']  # 单位邮编
        # del self.patient['linkman']       # 联系人
        # del self.patient['relationship']  # 关系
        # del self.patient['addr']          # 地址
        # del self.patient['tel']           # 电话
        # del self.patient['hbs']           # 血红蛋白SHBsAg
        # del self.patient['hcv']           # 丙型肝炎病毒抗HCV-IgG
        # del self.patient['hiv']           # 艾滋病病毒抗HIV
        # 年度变化指标另外存储（需要确定哪些必要）（入院的）
        # del self.excel['height']  # 身高
        # del self.excel['weight']  # 体重
        # del self.excel['BMI']     # BMI是年度变化指标，有多个

        # 新增删除
        del self.excel['education']
        # del self.excel['birth']
        del self.excel['age']
        del self.excel['deathdate']
        del self.excel['eventdate']
        # del self.excel['dateSt']
        del self.excel['dateEn']
        del self.excel['dateHD']
        del self.excel['dialysis']
        del self.excel['accessC']
        del self.excel['HBVDNA']
        del self.excel['antiRAAS']
        del self.excel['ACEIandARB']
        # del self.excel['αβblockers']
        del self.excel['ARBdiuretic']
        del self.excel['Pbinder']
        del self.excel['CVD']
        # 由于原数据这项属性为空，故删去
        del self.excel['TSAT']                   # 转铁蛋白饱和度


        # 这些是病人透析记录的（从基本信息中删除）
        del self.excel['HDpw']         # 每周透析次数
        del self.excel['HDFpw']        # 每周HDF次数
        del self.excel['sessiontime']  # 透析时间
        del self.excel['timepw']       # 每周透析时间
        del self.excel['dryweight']    # 干体重
        del self.excel['dialyser']     # 透析器
        # del self.excel['area']       # 透析器膜面积
        # del self.excel['highflux']   # 高通量透析
        # del self.excel['bloodflow']  # 血流量
        # 平均的基本不要
        del self.excel['preSBP']      # 平均透前收缩压
        del self.excel['preDBP']      # 平均透前舒张压
        del self.excel['preHR']       # 平均透前心率
        del self.excel['postSBP']     # 平均透后收缩压
        del self.excel['postDBP']     # 平均透后舒张压
        del self.excel['postHR']      # 平均透后心率
        del self.excel['preweight']   # 平均透前体重
        del self.excel['postweight']  # 平均透后体重
        del self.excel['UF']          # 平均超滤量
        # 这些透析记录都没有，当做基本信息来用
        # del self.excel['SDUFR']                  # 超滤量/干体重/透析时间
        # del self.excel['spKtV']
        # del self.excel['HBsAg']                  # 乙肝表面抗原
        # del self.excel['HBsAb']                  # 乙肝表面抗体
        # del self.excel['HBeAg']                  # 乙肝e抗原
        # del self.excel['HBeAb']                  # 乙肝e抗体
        # del self.excel['HBcAb']                  # 乙肝中心抗体
        # del self.excel['HCV']                    # 丙肝
        # del self.excel['HBVDNA']                 # 乙肝病毒DNA定量检测
        # del self.excel['HGB']                    # 血红蛋白
        # del self.excel['WBC']                    # 血白细胞
        # del self.excel['RBC']                    # 血红细胞
        # del self.excel['HCT']                    # 红细胞压积
        # del self.excel['MCV']                    # 红细胞平均容积
        # del self.excel['MCH']                    # 红细胞平均血红蛋白量
        # del self.excel['MCHC']                   # 红细胞平均血红蛋白浓度
        # del self.excel['PLT']                    # 血小板
        # del self.excel['NEUT']                   # 中性粒细胞百分率
        # del self.excel['LYMPH']                  # 淋巴细胞百分率
        # del self.excel['MONO']                   # 单核细胞百分率
        # del self.excel['LYMPHc']                 # 淋巴细胞计数
        # del self.excel['NEUTc']                  # 中性粒细胞计数
        # del self.excel['MONOc']                  # 单核细胞计数
        # del self.excel['RETHb']                  # 网炽红细胞血红蛋白量
        # del self.excel['ALT']                    # 谷丙转氨酶
        # del self.excel['AST']                    # 谷草转氨酶
        # del self.excel['GLU']                    # 随机血糖
        # del self.excel['Cl']                     # 氯
        # del self.excel['ALB']                    # 血清白蛋白
        # del self.excel['K']                      # 钾
        # del self.excel['Na']                     # 钠
        # del self.excel['Ca']                     # 钙
        # del self.excel['P']                      # 磷
        # del self.excel['HCO3']                   # 碳酸氢盐
        # del self.excel['BUN']                    # 尿素氮
        # del self.excel['Cr']                     # 肌酐
        # del self.excel['UA']                     # 尿酸
        # del self.excel['CRP']                    # C反应蛋白
        # del self.excel['postBUN']                # 透后尿素氮
        # del self.excel['Fe']                     # 铁
        # del self.excel['FER']                    # 血清铁蛋白
        # del self.excel['UIBC']                   # 血清不饱和铁结合力
        # del self.excel['TIBC']                   # 总铁结合力
        # del self.excel['TSAT']                   # 转铁蛋白饱和度
        # del self.excel['iPTH']                   # 全段甲状旁腺激素
        # del self.excel['CHOL']                   # 总胆固醇
        # del self.excel['TRIG']                   # 甘油三酯
        # del self.excel['HDL']                    # 高密度脂蛋白胆固醇
        # del self.excel['LDL']                    # 低密度脂蛋白胆固醇
        # del self.excel['Lpa']                    # 脂蛋白a
        # del self.excel['anticoagulant']          # 抗凝药
        # del self.excel['EPO']                    # 促红素
        # del self.excel['EPOdose']                # 促红素剂量
        # del self.excel['CCB']                    # 钙通道阻滞剂
        # del self.excel['ACEI']                   # 血管紧张素转换酶抑制剂
        # del self.excel['ARB']                    # 血管紧张素Ⅱ受体阻滞剂
        # del self.excel['antiRAAS']               # ACEI或ARB
        # del self.excel['ACEIandARB']             # ACEI和ARB
        # del self.excel[u'\u03b2blocker']         # β受体阻滞剂
        # del self.excel[u'\u03b1blocer']          # α受体阻滞剂
        # del self.excel[u'\u03b1\u03b2blockers']  # β受体阻滞剂和a受体阻滞剂
        # del self.excel['diuretic']               # 利尿剂
        # del self.excel['ARBdiuretic']            # ARB和利尿剂
        # del self.excel['LipidD']                 # 调脂药
        # del self.excel['CaPB']                   # 含钙的磷结合剂
        # del self.excel['NCaPB']                  # 不含钙的磷结合剂
        # del self.excel['Pbinder']                # 磷结合剂
        # del self.excel['VitD']                   # 活性维生素D3
        # del self.excel['mucosaprotect']          # 胃粘膜保护剂
        # del self.excel['H2RA']                   # H2受体拮抗剂
        # del self.excel['PPI']                    # 质子泵抑制剂
        # del self.excel['APUD']                   # 消化道溃疡相关用药
        # 这些是病人透析记录的（从基本信息中删除）
        del self.excel['LCVC']
        del self.excel['SCVC']
        del self.excel['AVF']
        del self.excel['AVG']
        del self.excel['puncture']
        # 新增删除
        # del self.excel['education']
        # del self.excel['birth']
        # del self.excel['dateSt']
        # del self.excel['dateEn']
        # del self.excel['dateHD']
        # del self.excel['dialysis']
        # del self.excel['accessC']
        # del self.excel['HBVDNA']
        # del self.excel['antiRAAS']
        # del self.excel['ACElandARB']
        # del self.excel['伪尾blockers']
        # del self.excel['ARBdiuretic']
        # del self.excel['Pbinder']
        # del self.excel['CVD']
        
        # merge：连接两个表的内容，类似数据库中的join
        self.patient['case_no'] = self.patient['case_no'].astype(np.str)
        self.excel['ID'] = self.excel['ID'].astype(np.str)  # 因为数据库里的case_no含有非数字，是string类型，所以把excel的统一成string，容易merge
        experiment_patient = pd.merge(self.patient, self.excel, how='inner', left_on='case_no', right_on='ID')
        print("merge...")
        print(experiment_patient)

        del experiment_patient['case_no']
        del experiment_patient['ID']
        del experiment_patient[ u'\u03b1\u03b2blockers']  
        experiment_patient.to_csv(patient_cleaned_path, encoding='UTF-8')  # 把病人数据重新保存
        print("merge over")

        # drop data
        # self.patient = pd.read_csv(r'cleaned/patient.csv', parse_dates=True, encoding='UTF-8')
        # self.patient.drop(['case_no','ID', u'\u03b1\u03b2blockers'], 
        #                    axis=1, inplace=True)
        # # print(self.patient)
        # self.patient.to_csv('cleaned/cleaned/patient.csv', encoding='UTF-8')
        # print('dropping patient data is over!')

        # # isin():判断该位置的值，是否在整个序列或者数组中，返回Ture或False
        # experiment_record = self.record[self.record['patient_id'].isin(experiment_patient['patient_id'])]
        # # 删除医生不建议的属性
        # del experiment_record['tx_code']
        # del experiment_record['tx_count']
        # del experiment_record['fill_nurse']
        # del experiment_record['bed_no']
        # del experiment_record['f3']
        # del experiment_record['vascular_access_pos']
        # del experiment_record['doctor']
        # del experiment_record['login_nurse']
        # del experiment_record['check_nurse']
        # del experiment_record['logout_nurse']
        # del experiment_record['record_nurse']
        # del experiment_record['diagnosis']
        # del experiment_record['first_dose']
        # del experiment_record['next_dose']
        # experiment_record.to_csv(record_cleaned_path, encoding='UTF-8')  # 把透析记录数据重新保存

        # experiment_item = self.item[self.item['tx_id'].isin(experiment_record['tx_id'])]
        # # 删除医生不建议的属性
        # del experiment_item['id']
        # del experiment_item['ultrafiltration_weight']
        # del experiment_item['heparin_amount']
        # del experiment_item['cd13']
        # del experiment_item['cd14']
        # del experiment_item['operator']
        # del experiment_item['nursing_record']
        # del experiment_item['cd17']
        # experiment_item.to_csv(item_cleaned_path, encoding='UTF-8')  # 把透析记录子项数据重新保存
        print("all over")

    

    def __balance_data(self,patient_cleaned_path,item_cleaned_path,record_cleaned_path):
        # 基本信息
        patient_file = patient_cleaned_path
        # patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0],
        #                        parse_dates=['begin_date', 'end_date', 'center_begin_date', 'tx_begin_date', 'eventdate',
        #                                     'vascular_access_build_date', 'birth', 'dateSt', 'dateEn', 'deathdate', 'dateHD'])
        # missing_abnormal()之后，删除了'birth', 'dateSt'
        patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0])
        print('Total lines: %d' % len(patients))
        # # 透析记录
        record_file = record_cleaned_path
        records = pd.read_csv(record_file, encoding='UTF-8', low_memory=False, index_col=[0],
                              parse_dates=['tx_date', 'target_treat_time', 'actual_treat_time'])
        print('Total lines: %d' % len(records))
        # 透析记录子项
        item_file = item_cleaned_path
        items = pd.read_csv(item_file, encoding='UTF-8', index_col=[0], parse_dates=['check_time'])
        print('Total lines: %d' % len(items))
        #
        # print(len(items.columns))
        # print(items.columns)
        # #
        patient_ids = set(records['patient_id'])
        # nullset = {'vascular_access_type', 'dialysis_machine', 'clean_machine', 'reuse_times', 'anticoagulation', 'target_treat_time', 'actual_treat_time', 'dry_weight',
        #            'pre_weight', 'target_ultrafiltration', 'after_weight', 'actual_ultrafiltration'}
        # 删除reuse_times
        nullset = {'vascular_access_type', 'dialysis_machine', 'clean_machine', 'anticoagulation', 'target_treat_time', 'actual_treat_time', 'dry_weight',
                   'pre_weight', 'target_ultrafiltration', 'after_weight', 'actual_ultrafiltration'}           
        nullid = set()
        for id in patient_ids:
            # print('id ', id)
            for col in records[records['patient_id'] == id].columns:
                # print('col:', col)
                # print('value number:', records[records['patient_id'] == id][col].value_counts())
                # print('length1:', len(records[records['patient_id'] == id][col].value_counts()))
                if (col in nullset) and (len(records[records['patient_id'] == id][col].value_counts())) == 0:  # 某个属性全为空，这个病人无法分析
                    # print('length2:', len(records[records['patient_id'] == id][col].value_counts()))
                    nullid.add(id)
                    
            # 经测试，每个病人的透析记录大于60条
            if (len(records[records['patient_id'] == id]))< 60:  # 如果一个病人透析记录少于60条，判为太少
                # print(id, len(records[records['patient_id'] == id])
                # print('data is less than 60')
                nullid.add(id)
        print(nullid)
        print('len(nullid):', len(nullid))
        # print(~pd.Series(records['patient_id'].unique()).isin(nullid))
        
        patients = patients[~patients['patient_id'].isin(nullid)]
        records = records[records['patient_id'].isin(patients['patient_id'])]
        items = items[items['tx_id'].isin(records['tx_id'])]
        # 输出：17 2150 15296
        print(len(patients), len(records), len(items))
        
        # records还要增加一个额外的计算属性（这是一个重要指标）
        # lambda 传入参数 ： 返回的计算表达式。按小时计算
        records['SDUFR'] = records['actual_ultrafiltration'] / \
                           records['dry_weight'] / \
                           (records['actual_treat_time'] - pd.to_datetime('1900-01-01')).map(lambda x: x.seconds / 3600.0)
        # 修改完成，重新写回
        patients.to_csv(patient_file, encoding='UTF-8')
        records.to_csv(record_file, encoding='UTF-8')
        items.to_csv(item_file, encoding='UTF-8')
        print('balance data is done')
    
    
    def __item_stats(self,patient_cleaned_path,item_cleaned_path,record_cleaned_path,record_file_return_path,item_result_path):  # 子项统计量
        # 基本信息
        patient_file = patient_cleaned_path
        # patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0],
        #                        parse_dates=['begin_date', 'end_date', 'center_begin_date', 'tx_begin_date', 'eventdate',
        #                                     'vascular_access_build_date', 'birth', 'dateSt', 'dateEn', 'deathdate', 'dateHD'])
        patients =  pd.read_csv(patient_file, encoding='UTF-8', index_col=[0])
        print('Total lines: %d' % len(patients))
        # 透析记录
        record_file = record_cleaned_path
        records = pd.read_csv(record_file, encoding='UTF-8', low_memory=False, index_col=[0],
                              parse_dates=['tx_date', 'target_treat_time', 'actual_treat_time'])
        print('Total lines: %d' % len(records))
        # 透析记录子项
        item_file = item_cleaned_path
        items = pd.read_csv(item_file, encoding='UTF-8', index_col=[0], parse_dates=['check_time', 'tx_date'])
        print('Total lines: %d' % len(items))
        # 为每次记录增加属性
        # 增加的属性为每个变量的均值、方差、极差、变化量累计
        items = items[['vein_pressure', 'membrane_pressure', 'blood_flow_volume', 'na_concentration', 'body_temperature',
                       'SBP', 'DBP', 'pulse', 'breathe', 'tx_id']]  # 只需要这些属性
        items['vein_pressure'] = (items['vein_pressure'] == '[>150]').astype(int)          # bool字段类型换成int型
        items['membrane_pressure'] = (items['membrane_pressure'] == '[>300]').astype(int)  # bool字段类型换成int型
        # 相应地增加均值、方差、极差、总变化幅度
        records['vein_mean'] = records['vein_var'] = records['vein_range'] = records['vein_change'] = np.nan
        records['membrane_mean'] = records['membrane_var'] = records['membrane_range'] = records['membrane_change'] = np.nan
        records['bloodf_mean'] = records['bloodf_var'] = records['bloodf_range'] = records['bloodf_change'] = np.nan
        records['na_mean'] = records['na_var'] = records['na_range'] = records['na_change'] = np.nan
        records['temperatrue_mean'] = records['temperatrue_var'] = records['temperatrue_range'] = records['temperatrue_change'] = np.nan
        records['sbp_mean'] = records['sbp_var'] = records['sbp_range'] = records['sbp_change'] = np.nan
        records['dbp_mean'] = records['dbp_var'] = records['dbp_range'] = records['dbp_change'] = np.nan
        records['pulse_mean'] = records['pulse_var'] = records['pulse_range'] = records['pulse_change'] = np.nan
        records['breathe_mean'] = records['breathe_var'] = records['breathe_range'] = records['breathe_change'] = np.nan
        
        # # pandas的处理函数
        # # diff函数是用来将数据进行某种移动之后与原数据进行比较得出的差异数据
        def get_value(df):
            df = pd.DataFrame(df)
            del df['tx_id']
            return pd.DataFrame({
                'mean': df.mean().values,
                'var': df.var().values,
                'range': (df.max() - df.min()).values,
                'change': df.diff().abs().sum().values
            }, index=['vein', 'membrane', 'bloodf', 'na', 'temperature', 'sbp', 'dbp', 'pulse', 'breathe'])
        # 下面这三句执行非常久
        items = items.fillna(0)                  # fillna(0)：以0填充缺失值
        itemgroup = items.groupby('tx_id')       # groupby('tx_id')：按tx_id分组
        item_stats = itemgroup.apply(get_value)  # apply来自定义函数求值
        # 所以使用HDFS赶紧把处理完的数据存起来，下次直接使用，节省时间
        # itemresult = pd.HDFStore('caches/itemresult.h5')
        # itemresult['item_stats'] = item_stats  # 这是存放进去
        item_result_path
        itemresult = pd.HDFStore(item_result_path, 'r')
        item_stats = itemresult['item_stats']    # 这是读取出来
        # print('HDFS done')

        # 打印demo
        # ix：行号及行标签索引
        # print item_stats['mean']
        # for tx_id in records.index:
        #     # item_stats['mean'].ix[tx_id, 'vein']
        #     # item_stats['var'].ix[tx_id, 'vein']
        #     # item_stats['range'].ix[tx_id, 'vein']
        #     # item_stats['change'].ix[tx_id, 'vein']
        #     break
        record_file_return = record_file_return_path
#        record_file_return = r'analysis_data/recorditem.csv'
        records.index = records['tx_id']
        # 这里的意思是，结果计算出来，但是要按照一定顺序取出来存成csv
        # ix：索引某行某列
        for tx_id in records.index:
            records.ix[tx_id, [
                'vein_mean', 'vein_var', 'vein_range', 'vein_change',
                'membrane_mean', 'membrane_var', 'membrane_range', 'membrane_change',
                'bloodf_mean', 'bloodf_var', 'bloodf_range', 'bloodf_change',
                'na_mean', 'na_var', 'na_range', 'na_change',
                'temperatrue_mean', 'temperatrue_var', 'temperatrue_range', 'temperatrue_change',
                'sbp_mean', 'sbp_var', 'sbp_range', 'sbp_change',
                'dbp_mean', 'dbp_var', 'dbp_range', 'dbp_change',
                'pulse_mean', 'pulse_var', 'pulse_range', 'pulse_change',
                'breathe_mean', 'breathe_var', 'breathe_range', 'breathe_change']] = [
                item_stats['mean'].ix[tx_id, 'vein'], item_stats['var'].ix[tx_id, 'vein'],
                item_stats['range'].ix[tx_id, 'vein'], item_stats['change'].ix[tx_id, 'vein'],
                item_stats['mean'].ix[tx_id, 'membrane'], item_stats['var'].ix[tx_id, 'membrane'],
                item_stats['range'].ix[tx_id, 'membrane'], item_stats['change'].ix[tx_id, 'membrane'],
                item_stats['mean'].ix[tx_id, 'bloodf'], item_stats['var'].ix[tx_id, 'bloodf'],
                item_stats['range'].ix[tx_id, 'bloodf'], item_stats['change'].ix[tx_id, 'bloodf'],
                item_stats['mean'].ix[tx_id, 'na'], item_stats['var'].ix[tx_id, 'na'],
                item_stats['range'].ix[tx_id, 'na'], item_stats['change'].ix[tx_id, 'na'],
                item_stats['mean'].ix[tx_id, 'temperature'], item_stats['var'].ix[tx_id, 'temperature'],
                item_stats['range'].ix[tx_id, 'temperature'], item_stats['change'].ix[tx_id, 'temperature'],
                item_stats['mean'].ix[tx_id, 'sbp'], item_stats['var'].ix[tx_id, 'sbp'],
                item_stats['range'].ix[tx_id, 'sbp'], item_stats['change'].ix[tx_id, 'sbp'],
                item_stats['mean'].ix[tx_id, 'dbp'], item_stats['var'].ix[tx_id, 'dbp'],
                item_stats['range'].ix[tx_id, 'dbp'], item_stats['change'].ix[tx_id, 'dbp'],
                item_stats['mean'].ix[tx_id, 'pulse'], item_stats['var'].ix[tx_id, 'pulse'],
                item_stats['range'].ix[tx_id, 'pulse'], item_stats['change'].ix[tx_id, 'pulse'],
                item_stats['mean'].ix[tx_id, 'breathe'], item_stats['var'].ix[tx_id, 'breathe'],
                item_stats['range'].ix[tx_id, 'breathe'], item_stats['change'].ix[tx_id, 'breathe']
            ]
        del records['tx_id']
        records.to_csv(record_file_return, encoding='UTF-8')
        print('item_stats is done')
    
    
    
    
    def __merge_and_fill_item(self,item_cleaned_path,record_cleaned_path):
        # 向item添加patient_id和tx_date
        item_file = item_cleaned_path
        # item_file1 = r'cleaned/cleaned/item1.csv'
        items = pd.read_csv(item_file, encoding='UTF-8', index_col=[0], parse_dates=['check_time'])
        record_file = record_cleaned_path
        records =  pd.read_csv(record_file, encoding='UTF-8', index_col=[0])

        # merge：连接两个表的内容，类似数据库中的join
        experiment_items = pd.merge(left=items, right=records, on='tx_id')
        # 删除不必要的属性，record.csv保存一份即可
        del experiment_items['subject']; del experiment_items['treat_item']; del experiment_items['vascular_access_type'];
        del experiment_items['dialysis_machine']; del experiment_items['clean_machine']; del experiment_items['anticoagulation_scope'];
        del experiment_items['anticoagulation']; del experiment_items['protamine']; del experiment_items['target_treat_time'];
        del experiment_items['actual_treat_time']; del experiment_items['replacement_way']; del experiment_items['replace_amount'];
        del experiment_items['ca_concentration']; del experiment_items['k_concentration']; del experiment_items['dry_weight'];
        del experiment_items['pre_weight']; del experiment_items['target_ultrafiltration']; del experiment_items['take_food'];
        del experiment_items['fluid_infusion']; del experiment_items['after_weight']; del experiment_items['actual_ultrafiltration'];
        del experiment_items['blood_pressure_pos']; del experiment_items['SDUFR']
        
        experiment_items.to_csv(item_file, encoding='UTF-8')  # 把item数据重新保存
        print("item and record merge over")

        # fill
        items = pd.read_csv(item_file, encoding='UTF-8', index_col=[0], parse_dates=['check_time', 'tx_date'])
        print('start ffill & bfill...')
        patient_ids = set(items['patient_id'])
        try:
            for id in patient_ids:
                items.loc[items['patient_id'] == id] = \
                    items.loc[items['patient_id'] == id].sort_values(by=['tx_date'], ascending=True).fillna(method='ffill').fillna(method='bfill')
        except:
            # 发出警告，没有抛出异常，为什么？
            print('ffill & bfill have failed')
        items.to_csv(item_file, encoding='UTF-8')
        print("items fill has over")