# -*- coding: utf-8 -*-

class BuildDTService:
    def __init__(self):
        print("BuildDTService")
    
    def build_dataset1(self):
        """
        小数据集构建
        :return:
        """
        patient_file = r'cleaned/cleaned/patient.csv'
        # patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0],
        #                        parse_dates=['begin_date', 'end_date', 'center_begin_date', 'tx_begin_date', 'eventdate',
        #                                     'vascular_access_build_date', 'birth', 'dateSt', 'dateEn', 'deathdate', 'dateHD'])
        patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0])
        print('Total lines: %d' % len(patients))
        # 有些属性有意义，但是暂时分析不了
        # del patients['case_no']; del patients['begin_date']; del patients['end_date']; del patients['in_diagnosis']
        # del patients['center_begin_date']; del patients['tx_begin_date']; del patients['begin_unit']; del patients['vascular_access_type']
        # del patients['vascular_access_build_date']; del patients['ID']; del patients['birth']; del patients['dateSt']
        # del patients['dateEn']; del patients['age']; del patients['education']; del patients['deathdate']; del patients['eventdate']
        # del patients['dateHD']; del patients['accessC']; del patients['dialysis']; del patients['HBVDNA']
        # del patients['antiRAAS']; del patients['ACEIandARB'];del patients[u'\u03b1\u03b2blockers']; del patients['ARBdiuretic']
        # del patients['Pbinder']; del patients['CVD']
        # 不是0、1、3、4，而是0、1、2、3
        patients['marital'] = patients['marital'].map({0: 0, 1: 1, 3: 2, 4: 3})

        print(len(patients.columns))
        for col in patients.columns:
            print(col, patients[col].dtype, *list(patients[col].unique())) # unique()去重  

        record_file = r'analysis_data/recorditem.csv'
        # index_col将年月日的哪个作为索引;parse_dates指定日期在哪列 
        records = pd.read_csv(record_file, encoding='UTF-8', low_memory=False, index_col=[0],
                              parse_dates=['tx_date', 'target_treat_time', 'actual_treat_time'])
        print('Total lines: %d' % len(records))
        # 下面是分类变量，所以删了
        del records['vein_mean']
        del records['vein_var']
        del records['vein_range']
        del records['membrane_mean']
        del records['membrane_var']
        del records['membrane_range']
        print(len(records.columns))
        print(records.columns)
        for index, col in enumerate(records.columns):
            print(index+1, col, records[col].dtype, *(list(records[col].unique())[: 10]))

        records['tx_id'] = records.index
        records.index = records['tx_date']

        records['vascular_access_type'] = records['vascular_access_type'].map({
            'AVF': 0, 'SCVC': 1, 'puncture': 2, 'LCVC': 3, 'AVG': 4
        })
        records['dialysis_machine'] = records['dialysis_machine'].map({
            'FSYS': 0, 'BT': 1, 'TL': 2, 'JB': 3, 'BL': 4
        })
        records['clean_machine'] = (records['clean_machine'] == '[>1.5]').astype(int)
        records['ca_concentration'] = records['ca_concentration'].map({
            '[1.25]': 0, '[1.5]': 1, '[1.75]': 2
        })
        records['k_concentration'] = (records['k_concentration'] == '[>=3.0]').astype(int)
        records['target_treat_time'] = (records['target_treat_time'] - pd.to_datetime('1900-01-01')).map(lambda x: x.seconds / 3600.0)
        records['actual_treat_time'] = (records['actual_treat_time'] - pd.to_datetime('1900-01-01')).map(lambda x: x.seconds / 3600.0)

        # def get_value(dataframe):  # 统计量
            # dataframe = pd.DataFrame(dataframe)
            # del dataframe['patient_id']
            # del dataframe['tx_date']
            # return pd.DataFrame({
            #     'mean': dataframe.mean().values,
            #     'var': dataframe.var().values,
            #     'range': (dataframe.max() - dataframe.min()).values,
            #     'change': (dataframe.diff() != 0).astype(int).sum().values
            # }, index=['subject', 'treat_item', 'access', 'dmachine', 'cmachine',
            #           'reuse', 'anti_scope', 'anti', 'protamine', 'target_time',
            #           'actual_time', 'rway', 'ramount', 'ca', 'k', 'dry_w',
            #           'pre_w', 'target_ultra', 'food', 'fluid', 'after_w',
            #           'actual_ultra', 'bloodpos', 'SDUFR', 'vein_change',
            #           'membrane_change', 'bloodf_mean', 'bloodf_var',
            #           'bloodf_range', 'bloodf_change', 'na_mean', 'na_var',
            #           'na_range', 'na_change', 't_mean', 't_var', 't_range',
            #           't_change', 'sbp_mean', 'sbp_var', 'sbp_range',
            #           'sbp_change', 'dbp_mean', 'dbp_var', 'dbp_range',
            #           'dbp_change', 'pulse_mean', 'pulse_var', 'pulse_range',
            #           'pulse_change', 'bre_mean', 'bre_var', 'bre_range',
            #           'bre_change'])
        # 需要进行时间序列分析的属性
        # arima_columns = ['target_treat_time', 'actual_treat_time', 'replace_amount', 'dry_weight', 'pre_weight',
        #                 'target_ultrafiltration', 'after_weight', 'actual_ultrafiltration', 'SDUFR',
        #                 'vein_change', 'membrane_change', 'bloodf_mean', 'bloodf_var', 'bloodf_range', 'bloodf_change',
        #                 'na_mean', 'na_var', 'na_range', 'na_change', 'temperatrue_mean', 'temperatrue_var',
        #                 'temperatrue_range', 'temperatrue_change', 'sbp_mean', 'sbp_var', 'sbp_range', 'sbp_change',
        #                 'dbp_mean', 'dbp_var', 'dbp_range', 'dbp_change', 'pulse_mean', 'pulse_var', 'pulse_range',
        #                 'pulse_change', 'breathe_mean', 'breathe_var', 'breathe_range', 'breathe_change']

        # def get_arima(dataframe):
        #     """
        #     时间序列分析，但是有点久，最好还是保存中间数据
        #     :param dataframe:
        #     :return:
        #     """
        #     print('IN GET_ARIMA-------------------------------------------------------------------------------------')
        #     dataframe = pd.DataFrame(dataframe)
        #     del dataframe['patient_id']
        #     dataframe.index = dataframe['tx_date']
        #     del dataframe['tx_date']
        #     result = pd.DataFrame(np.zeros((len(arima_columns), 3)), index=arima_columns, columns=list('pdq'))
        #     # ADF检验
        #     for col in arima_columns:
        #         diff = 0
        #         try:
        #             adf = ADF(dataframe[col])
        #         except Exception:
        #             result.ix[col, ['p', 'd', 'q']] = [0, 0, 0]
        #             continue
        #         is_except = False
        #         # adf[1]表示p值
        #         while adf[1] >= 0.05:
        #             diff = diff + 1
        #             try:
        #                 # 差分后，前几行的数据会变成nan，所以删掉。nan会导致ARMA无法拟合。
        #                 adf = ADF(dataframe[col].diff(diff).dropna())
        #             except Exception:
        #                 result.ix[col, ['p', 'd', 'q']] = [0, 0, 0]
        #                 is_except = True
        #                 break
        #         if is_except:
        #             result.ix[col, ['p', 'd', 'q']] = [0, diff, 0]
        #             continue
        #         if diff == 0:
        #             # acorr_ljungbox：随机性检验（白噪声）
        #             [[lb], [p]] = acorr_ljungbox(dataframe[col], lags=1) # lags：表示滞后的阶数
        #         else:
        #             [[lb], [p]] = acorr_ljungbox(dataframe[col].diff(diff), lags=1)
        #         is_noise = (p >= 0.05)
        #         if (diff == 0 and is_noise) or (diff != 0 and not is_noise):
        #             result.ix[col, ['p', 'd', 'q']] = [0, 0, 0]
        #             continue

        #         # if diff != 0 and not is_noise:
        #         #     while not is_noise:
        #         #         diff += 1
        #         #         [[lb], [p]] = acorr_ljungbox(dataframe[col].diff(diff), lags=1)
        #         #         is_noise = (p >= 0.05)

        #         # 定阶
        #         pmax = int(len(dataframe[col]) / 10)
        #         qmax = int(len(dataframe[col]) / 10)
        #         pmax = qmax = 5
        #         bic_matrix = list()
        #         # BIC定阶
        #         for p in range(pmax + 1):
        #             temp = list()
        #             for q in range(qmax + 1):
        #                 try:
        #                     # mle：通过卡尔曼滤波器最大化精确的似然
        #                     temp.append(ARIMA(dataframe[col], (p, diff, q)).fit(method='mle', disp=-1).bic)
        #                 except:
        #                     temp.append(None)
        #             bic_matrix.append(temp)
        #         bic_matrix = pd.DataFrame(bic_matrix)
        #         try:
        #             # 求bic_matrix最小的行列标
        #             p, q = bic_matrix.stack().idxmin()
        #         except Exception:
        #             p = q = 0
        #         result.ix[col, ['p', 'd', 'q']] = [p, diff, q]
        #     return result

        # recordgroup = records.groupby('patient_id')
        # # recordstats = recordgroup.apply(get_value)
        # recordarima = recordgroup.apply(get_arima)

        # 所以使用HDFS赶紧把处理完的数据存起来，下次直接使用，节省时间
        # recordsult1 = pd.HDFStore('caches/data1_stats.h5')
        # recordsult1['recordstats'] = recordstats  # 这是存放进去
        # recordsult2 = pd.HDFStore('caches/data1_arima.h5')
        # recordsult2['recordarima'] = recordarima  # 这是存放进去
        recordsult1 = pd.HDFStore('caches/data1_stats.h5', 'r')
        recordstats = recordsult1['recordstats']    # 这是读取出来
        recordsult2 = pd.HDFStore('caches/data1_arima.h5', 'r')
        recordarima = recordsult2['recordarima']    # 这是读取出来
        print('HDFS done')

        patients['subject_change'] = np.nan
        patients['treatitem_change'] = np.nan
        patients['access_change'] = np.nan
        patients['dmachine_change'] = np.nan
        patients['cmachine_change'] = np.nan
        patients['reuse_change'] = np.nan
        patients['antiscope_change'] = np.nan
        patients['anti_change'] = np.nan
        patients['protamine_change'] = np.nan
        patients['ttime_mean'] = patients['ttime_var'] = patients['ttime_range'] = patients['ttime_change'] = np.nan
        patients['ttime_p'] = patients['ttime_d'] = patients['ttime_q'] = np.nan
        patients['atime_mean'] = patients['atime_var'] = patients['atime_range'] = patients['atime_change'] = np.nan
        patients['atime_p'] = patients['atime_d'] = patients['atime_q'] = np.nan
        patients['rway_change'] = np.nan
        patients['ramount_mean'] = patients['ramount_var'] = patients['ramount_range'] = patients['ramount_change'] = np.nan
        patients['ramount_p'] = patients['ramount_d'] = patients['ramount_q'] = np.nan
        patients['ca_change'] = np.nan
        patients['k_change'] = np.nan
        patients['dryw_mean'] = patients['dryw_var'] = patients['dryw_range'] = patients['dryw_change'] = np.nan
        patients['dryw_p'] = patients['dryw_d'] = patients['dryw_q'] = np.nan
        patients['prew_mean'] = patients['prew_var'] = patients['prew_range'] = patients['prew_change'] = np.nan
        patients['prew_p'] = patients['prew_d'] = patients['prew_q'] = np.nan
        patients['tultra_mean'] = patients['tultra_var'] = patients['tultra_range'] = patients['tultra_change'] = np.nan
        patients['tultra_p'] = patients['tultra_d'] = patients['tultra_q'] = np.nan
        patients['food_change'] = np.nan
        patients['fluid_change'] = np.nan
        patients['afterw_mean'] = patients['afterw_var'] = patients['afterw_range'] = patients['afterw_change'] = np.nan
        patients['afterw_p'] = patients['afterw_d'] = patients['afterw_q'] = np.nan
        patients['aultra_mean'] = patients['aultra_var'] = patients['aultra_range'] = patients['aultra_change'] = np.nan
        patients['aultra_p'] = patients['aultra_d'] = patients['aultra_q'] = np.nan
        patients['bloodpos_change'] = np.nan
        patients['SDUFR_mean'] = patients['SDUFR_var'] = patients['SDUFR_range'] = patients['SDUFR_change'] = np.nan
        patients['SDUFR_p'] = patients['SDUFR_d'] = patients['SDUFR_q'] = np.nan
        patients['veinc_mean'] = patients['veinc_var'] = patients['veinc_range'] = patients['veinc_change'] = np.nan
        patients['veinc_p'] = patients['veinc_d'] = patients['veinc_q'] = np.nan
        patients['membc_mean'] = patients['membc_var'] = patients['membc_range'] = patients['membc_change'] = np.nan
        patients['membc_p'] = patients['membc_d'] = patients['membc_q'] = np.nan
        patients['bflowm_mean'] = patients['bflowm_var'] = patients['bflowm_range'] = patients['bflowm_change'] = np.nan
        patients['bflowm_p'] = patients['bflowm_d'] = patients['bflowm_q'] = np.nan
        patients['bflowv_mean'] = patients['bflowv_var'] = patients['bflowv_range'] = patients['bflowv_change'] = np.nan
        patients['bflowv_p'] = patients['bflowv_d'] = patients['bflowv_q'] = np.nan
        patients['bflowr_mean'] = patients['bflowr_var'] = patients['bflowr_range'] = patients['bflowr_change'] = np.nan
        patients['bflowr_p'] = patients['bflowr_d'] = patients['bflowr_q'] = np.nan
        patients['bflowc_mean'] = patients['bflowc_var'] = patients['bflowc_range'] = patients['bflowc_change'] = np.nan
        patients['bflowc_p'] = patients['bflowc_d'] = patients['bflowc_q'] = np.nan
        patients['nam_mean'] = patients['nam_var'] = patients['nam_range'] = patients['nam_change'] = np.nan
        patients['nam_p'] = patients['nam_d'] = patients['nam_q'] = np.nan
        patients['nav_mean'] = patients['nav_var'] = patients['nav_range'] = patients['nav_change'] = np.nan
        patients['nav_p'] = patients['nav_d'] = patients['nav_q'] = np.nan
        patients['nar_mean'] = patients['nar_var'] = patients['nar_range'] = patients['nar_change'] = np.nan
        patients['nar_p'] = patients['nar_d'] = patients['nar_q'] = np.nan
        patients['nac_mean'] = patients['nac_var'] = patients['nac_range'] = patients['nac_change'] = np.nan
        patients['nac_p'] = patients['nac_d'] = patients['nac_q'] = np.nan
        patients['tempm_mean'] = patients['tempm_var'] = patients['tempm_range'] = patients['tempm_change'] = np.nan
        patients['tempm_p'] = patients['tempm_d'] = patients['tempm_q'] = np.nan
        patients['tempv_mean'] = patients['tempv_var'] = patients['tempv_range'] = patients['tempv_change'] = np.nan
        patients['tempv_p'] = patients['tempv_d'] = patients['tempv_q'] = np.nan
        patients['tempr_mean'] = patients['tempr_var'] = patients['tempr_range'] = patients['tempr_change'] = np.nan
        patients['tempr_p'] = patients['tempr_d'] = patients['tempr_q'] = np.nan
        patients['tempc_mean'] = patients['tempc_var'] = patients['tempc_range'] = patients['tempc_change'] = np.nan
        patients['tempc_p'] = patients['tempc_d'] = patients['tempc_q'] = np.nan
        patients['sbpm_mean'] = patients['sbpm_var'] = patients['sbpm_range'] = patients['sbpm_change'] = np.nan
        patients['sbpm_p'] = patients['sbpm_d'] = patients['sbpm_q'] = np.nan
        patients['sbpv_mean'] = patients['sbpv_var'] = patients['sbpv_range'] = patients['sbpv_change'] = np.nan
        patients['sbpv_p'] = patients['sbpv_d'] = patients['sbpv_q'] = np.nan
        patients['sbpr_mean'] = patients['sbpr_var'] = patients['sbpr_range'] = patients['sbpr_change'] = np.nan
        patients['sbpr_p'] = patients['sbpr_d'] = patients['sbpr_q'] = np.nan
        patients['sbpc_mean'] = patients['sbpc_var'] = patients['sbpc_range'] = patients['sbpc_change'] = np.nan
        patients['sbpc_p'] = patients['sbpc_d'] = patients['sbpc_q'] = np.nan
        patients['dbpm_mean'] = patients['dbpm_var'] = patients['dbpm_range'] = patients['dbpm_change'] = np.nan
        patients['dbpm_p'] = patients['dbpm_d'] = patients['dbpm_q'] = np.nan
        patients['dbpv_mean'] = patients['dbpv_var'] = patients['dbpv_range'] = patients['dbpv_change'] = np.nan
        patients['dbpv_p'] = patients['dbpv_d'] = patients['dbpv_q'] = np.nan
        patients['dbpr_mean'] = patients['dbpr_var'] = patients['dbpr_range'] = patients['dbpr_change'] = np.nan
        patients['dbpr_p'] = patients['dbpr_d'] = patients['dbpr_q'] = np.nan
        patients['dbpc_mean'] = patients['dbpc_var'] = patients['dbpc_range'] = patients['dbpc_change'] = np.nan
        patients['dbpc_p'] = patients['dbpc_d'] = patients['dbpc_q'] = np.nan
        patients['pulsem_mean'] = patients['pulsem_var'] = patients['pulsem_range'] = patients['pulsem_change'] = np.nan
        patients['pulsem_p'] = patients['pulsem_d'] = patients['pulsem_q'] = np.nan
        patients['pulsev_mean'] = patients['pulsev_var'] = patients['pulsev_range'] = patients['pulsev_change'] = np.nan
        patients['pulsev_p'] = patients['pulsev_d'] = patients['pulsev_q'] = np.nan
        patients['pulser_mean'] = patients['pulser_var'] = patients['pulser_range'] = patients['pulser_change'] = np.nan
        patients['pulser_p'] = patients['pulser_d'] = patients['pulser_q'] = np.nan
        patients['pulsec_mean'] = patients['pulsec_var'] = patients['pulsec_range'] = patients['pulsec_change'] = np.nan
        patients['pulsec_p'] = patients['pulsec_d'] = patients['pulsec_q'] = np.nan
        patients['bream_mean'] = patients['bream_var'] = patients['bream_range'] = patients['bream_change'] = np.nan
        patients['bream_p'] = patients['bream_d'] = patients['bream_q'] = np.nan
        patients['breav_mean'] = patients['breav_var'] = patients['breav_range'] = patients['breav_change'] = np.nan
        patients['breav_p'] = patients['breav_d'] = patients['breav_q'] = np.nan
        patients['brear_mean'] = patients['brear_var'] = patients['brear_range'] = patients['brear_change'] = np.nan
        patients['brear_p'] = patients['brear_d'] = patients['brear_q'] = np.nan
        patients['breac_mean'] = patients['breac_var'] = patients['breac_range'] = patients['breac_change'] = np.nan
        patients['breac_p'] = patients['breac_d'] = patients['breac_q'] = np.nan

        dataset1 = r'analysis_data/dataset1.csv'
        patients.index = patients['patient_id']
        # 多一列patient_id
        # del patients['patient_id']

        # 下面是时间特征和统计量特征的保存
        for patient_id in patients.index:
            # try:
            #     patients.ix[patient_id, ['ttime_p', 'ttime_d', 'ttime_q']] = [
            #         recordarima['p'].ix[patient_id, 'target_treat_time'], recordarima['d'].ix[patient_id, 'target_treat_item'], recordarima['q'].ix[patient_id, 'target_treat_time']
            #     ]
            # except:
            #     print(patient_id)
            #     exit(0)
            # continue
            patients.ix[patient_id, [
                'ttime_p', 'ttime_d', 'ttime_q',
                'atime_p', 'atime_d', 'atime_q',
                'ramount_p', 'ramount_d', 'ramount_q',
                'dryw_p', 'dryw_d', 'dryw_q',
                'prew_p', 'prew_d', 'prew_q',
                'tultra_p', 'tultra_d', 'tultra_q',
                'afterw_p', 'afterw_d', 'afterw_q',
                'aultra_p', 'aultra_d', 'aultra_q',
                'SDUFR_p', 'SDUFR_d', 'SDUFR_q',
                'veinc_p', 'veinc_d', 'veinc_q',
                'membc_p', 'membc_d', 'membc_q',
                'bflowm_p', 'bflowm_d', 'bflowm_q',
                'bflowv_p', 'bflowv_d', 'bflowv_q',
                'bflowr_p', 'bflowr_d', 'bflowr_q',
                'bflowc_p', 'bflowc_d', 'bflowc_q',
                'nam_p', 'nam_d', 'nam_q',
                'nav_p', 'nav_d', 'nav_q',
                'nar_p', 'nar_d', 'nar_q',
                'nac_p', 'nac_d', 'nac_q',
                'tempm_p', 'tempm_d', 'tempm_q',
                'tempv_p', 'tempv_d', 'tempv_q',
                'tempr_p', 'tempr_d', 'tempr_q',
                'tempc_p', 'tempc_d', 'tempc_q',
                'sbpm_p', 'sbpm_d', 'sbpm_q',
                'sbpv_p', 'sbpv_d', 'sbpv_q',
                'sbpr_p', 'sbpr_d', 'sbpr_q',
                'sbpc_p', 'sbpc_d', 'sbpc_q',
                'dbpm_p', 'dbpm_d', 'dbpm_q',
                'dbpv_p', 'dbpv_d', 'dbpv_q',
                'dbpr_p', 'dbpr_d', 'dbpr_q',
                'dbpc_p', 'dbpc_d', 'dbpc_q',
                'pulsem_p', 'pulsem_d', 'pulsem_q',
                'pulsev_p', 'pulsev_d', 'pulsev_q',
                'pulser_p', 'pulser_d', 'pulser_q',
                'pulsec_p', 'pulsec_d', 'pulsec_q',
                'bream_p', 'bream_d', 'bream_q',
                'breav_p', 'breav_d', 'breav_q',
                'brear_p', 'brear_d', 'brear_q',
                'breac_p', 'breac_d', 'breac_q'
            ]] = [
                recordarima['p'].ix[patient_id, 'target_treat_time'], recordarima['d'].ix[patient_id, 'target_treat_time'], recordarima['q'].ix[patient_id, 'target_treat_time'],
                recordarima['p'].ix[patient_id, 'actual_treat_time'], recordarima['d'].ix[patient_id, 'actual_treat_time'], recordarima['q'].ix[patient_id, 'actual_treat_time'],
                recordarima['p'].ix[patient_id, 'replace_amount'], recordarima['d'].ix[patient_id, 'replace_amount'], recordarima['q'].ix[patient_id, 'replace_amount'],
                recordarima['p'].ix[patient_id, 'dry_weight'], recordarima['d'].ix[patient_id, 'dry_weight'], recordarima['q'].ix[patient_id, 'dry_weight'],
                recordarima['p'].ix[patient_id, 'pre_weight'], recordarima['d'].ix[patient_id, 'pre_weight'], recordarima['q'].ix[patient_id, 'pre_weight'],
                recordarima['p'].ix[patient_id, 'target_ultrafiltration'], recordarima['d'].ix[patient_id, 'target_ultrafiltration'], recordarima['q'].ix[patient_id, 'target_ultrafiltration'],
                recordarima['p'].ix[patient_id, 'after_weight'], recordarima['d'].ix[patient_id, 'after_weight'], recordarima['q'].ix[patient_id, 'after_weight'],
                recordarima['p'].ix[patient_id, 'actual_ultrafiltration'], recordarima['d'].ix[patient_id, 'actual_ultrafiltration'], recordarima['q'].ix[patient_id, 'actual_ultrafiltration'],
                recordarima['p'].ix[patient_id, 'SDUFR'], recordarima['d'].ix[patient_id, 'SDUFR'], recordarima['q'].ix[patient_id, 'SDUFR'],
                recordarima['p'].ix[patient_id, 'vein_change'], recordarima['d'].ix[patient_id, 'vein_change'], recordarima['q'].ix[patient_id, 'vein_change'],
                recordarima['p'].ix[patient_id, 'membrane_change'], recordarima['d'].ix[patient_id, 'membrane_change'], recordarima['q'].ix[patient_id, 'membrane_change'],
                recordarima['p'].ix[patient_id, 'bloodf_mean'], recordarima['d'].ix[patient_id, 'bloodf_mean'], recordarima['q'].ix[patient_id, 'bloodf_mean'],
                recordarima['p'].ix[patient_id, 'bloodf_var'], recordarima['d'].ix[patient_id, 'bloodf_var'], recordarima['q'].ix[patient_id, 'bloodf_var'],
                recordarima['p'].ix[patient_id, 'bloodf_range'], recordarima['d'].ix[patient_id, 'bloodf_range'], recordarima['q'].ix[patient_id, 'bloodf_range'],
                recordarima['p'].ix[patient_id, 'bloodf_change'], recordarima['d'].ix[patient_id, 'bloodf_change'], recordarima['q'].ix[patient_id, 'bloodf_change'],
                recordarima['p'].ix[patient_id, 'na_mean'], recordarima['d'].ix[patient_id, 'na_mean'], recordarima['q'].ix[patient_id, 'na_mean'],
                recordarima['p'].ix[patient_id, 'na_var'], recordarima['d'].ix[patient_id, 'na_var'], recordarima['q'].ix[patient_id, 'na_var'],
                recordarima['p'].ix[patient_id, 'na_range'], recordarima['d'].ix[patient_id, 'na_range'], recordarima['q'].ix[patient_id, 'na_range'],
                recordarima['p'].ix[patient_id, 'na_change'], recordarima['d'].ix[patient_id, 'na_change'], recordarima['q'].ix[patient_id, 'na_change'],
                recordarima['p'].ix[patient_id, 'temperatrue_mean'], recordarima['d'].ix[patient_id, 'temperatrue_mean'], recordarima['q'].ix[patient_id, 'temperatrue_mean'],
                recordarima['p'].ix[patient_id, 'temperatrue_var'], recordarima['d'].ix[patient_id, 'temperatrue_var'], recordarima['q'].ix[patient_id, 'temperatrue_var'],
                recordarima['p'].ix[patient_id, 'temperatrue_range'], recordarima['d'].ix[patient_id, 'temperatrue_range'], recordarima['q'].ix[patient_id, 'temperatrue_range'],
                recordarima['p'].ix[patient_id, 'temperatrue_change'], recordarima['d'].ix[patient_id, 'temperatrue_change'], recordarima['q'].ix[patient_id, 'temperatrue_change'],
                recordarima['p'].ix[patient_id, 'sbp_mean'], recordarima['d'].ix[patient_id, 'sbp_mean'], recordarima['q'].ix[patient_id, 'sbp_mean'],
                recordarima['p'].ix[patient_id, 'sbp_var'], recordarima['d'].ix[patient_id, 'sbp_var'], recordarima['q'].ix[patient_id, 'sbp_var'],
                recordarima['p'].ix[patient_id, 'sbp_range'], recordarima['d'].ix[patient_id, 'sbp_range'], recordarima['q'].ix[patient_id, 'sbp_range'],
                recordarima['p'].ix[patient_id, 'sbp_change'], recordarima['d'].ix[patient_id, 'sbp_change'], recordarima['q'].ix[patient_id, 'sbp_change'],
                recordarima['p'].ix[patient_id, 'dbp_mean'], recordarima['d'].ix[patient_id, 'dbp_mean'], recordarima['q'].ix[patient_id, 'dbp_mean'],
                recordarima['p'].ix[patient_id, 'dbp_var'], recordarima['d'].ix[patient_id, 'dbp_var'], recordarima['q'].ix[patient_id, 'dbp_var'],
                recordarima['p'].ix[patient_id, 'dbp_range'], recordarima['d'].ix[patient_id, 'dbp_range'], recordarima['q'].ix[patient_id, 'dbp_range'],
                recordarima['p'].ix[patient_id, 'dbp_change'], recordarima['d'].ix[patient_id, 'dbp_change'], recordarima['q'].ix[patient_id, 'dbp_change'],
                recordarima['p'].ix[patient_id, 'pulse_mean'], recordarima['d'].ix[patient_id, 'pulse_mean'], recordarima['q'].ix[patient_id, 'pulse_mean'],
                recordarima['p'].ix[patient_id, 'pulse_var'], recordarima['d'].ix[patient_id, 'pulse_var'], recordarima['q'].ix[patient_id, 'pulse_var'],
                recordarima['p'].ix[patient_id, 'pulse_range'], recordarima['d'].ix[patient_id, 'pulse_range'], recordarima['q'].ix[patient_id, 'pulse_range'],
                recordarima['p'].ix[patient_id, 'pulse_change'], recordarima['d'].ix[patient_id, 'pulse_change'], recordarima['q'].ix[patient_id, 'pulse_change'],
                recordarima['p'].ix[patient_id, 'breathe_mean'], recordarima['d'].ix[patient_id, 'breathe_mean'], recordarima['q'].ix[patient_id, 'breathe_mean'],
                recordarima['p'].ix[patient_id, 'breathe_var'], recordarima['d'].ix[patient_id, 'breathe_var'], recordarima['q'].ix[patient_id, 'breathe_var'],
                recordarima['p'].ix[patient_id, 'breathe_range'], recordarima['d'].ix[patient_id, 'breathe_range'], recordarima['q'].ix[patient_id, 'breathe_range'],
                recordarima['p'].ix[patient_id, 'breathe_change'], recordarima['d'].ix[patient_id, 'breathe_change'], recordarima['q'].ix[patient_id, 'breathe_change']
            ]
        for patient_id in patients.index:
            patients.ix[patient_id, [
                'subject_change', 'treatitem_change', 'access_change', 'dmachine_change', 'cmachine_change',
                'reuse_change', 'antiscope_change', 'anti_change', 'protamine_change',
                'ttime_mean', 'ttime_var', 'ttime_range', 'ttime_change',
                'atime_mean', 'atime_var', 'atime_range', 'atime_change',
                'rway_change',
                'ramount_mean', 'ramount_var', 'ramount_range', 'ramount_change',
                'ca_change', 'k_change',
                'dryw_mean', 'dryw_var', 'dryw_range', 'dryw_change',
                'prew_mean', 'prew_var', 'prew_range', 'prew_change',
                'tultra_mean', 'tultra_var', 'tultra_range', 'tultra_change',
                'food_change', 'fluid_change',
                'afterw_mean', 'afterw_var', 'afterw_range', 'afterw_change',
                'aultra_mean', 'aultra_var', 'aultra_range', 'aultra_change',
                'bloodpos_change',
                'SDUFR_mean', 'SDUFR_var', 'SDUFR_range', 'SDUFR_change',
                'veinc_mean', 'veinc_var', 'veinc_range', 'veinc_change',
                'membc_mean', 'membc_var', 'membc_range', 'membc_change',
                'bflowm_mean', 'bflowm_var', 'bflowm_range', 'bflowm_change',
                'bflowv_mean', 'bflowv_var', 'bflowv_range', 'bflowv_change',
                'bflowr_mean', 'bflowr_var', 'bflowr_range', 'bflowr_change',
                'bflowc_mean', 'bflowc_var', 'bflowc_range', 'bflowc_change',
                'nam_mean', 'nam_var', 'nam_range', 'nam_change',
                'nav_mean', 'nav_var', 'nav_range', 'nav_change',
                'nar_mean', 'nar_var', 'nar_range', 'nar_change',
                'nac_mean', 'nac_var', 'nac_range', 'nac_change',
                'tempm_mean', 'tempm_var', 'tempm_range', 'tempm_change',
                'tempv_mean', 'tempv_var', 'tempv_range', 'tempv_change',
                'tempr_mean', 'tempr_var', 'tempr_range', 'tempr_change',
                'tempc_mean', 'tempc_var', 'tempc_range', 'tempc_change',
                'sbpm_mean', 'sbpm_var', 'sbpm_range', 'sbpm_change',
                'sbpv_mean', 'sbpv_var', 'sbpv_range', 'sbpv_change',
                'sbpr_mean', 'sbpr_var', 'sbpr_range', 'sbpr_change',
                'sbpc_mean', 'sbpc_var', 'sbpc_range', 'sbpc_change',
                'dbpm_mean', 'dbpm_var', 'dbpm_range', 'dbpm_change',
                'dbpv_mean', 'dbpv_var', 'dbpv_range', 'dbpv_change',
                'dbpr_mean', 'dbpr_var', 'dbpr_range', 'dbpr_change',
                'dbpc_mean', 'dbpc_var', 'dbpc_range', 'dbpc_change',
                'pulsem_mean', 'pulsem_var', 'pulsem_range', 'pulsem_change',
                'pulsev_mean', 'pulsev_var', 'pulsev_range', 'pulsev_change',
                'pulser_mean', 'pulser_var', 'pulser_range', 'pulser_change',
                'pulsec_mean', 'pulsec_var', 'pulsec_range', 'pulsec_change',
                'bream_mean', 'bream_var', 'bream_range', 'bream_change',
                'breav_mean', 'breav_var', 'breav_range', 'breav_change',
                'brear_mean', 'brear_var', 'brear_range', 'brear_change',
                'breac_mean', 'breac_var', 'breac_range', 'breac_change'
            ]] = [
                recordstats['change'].ix[patient_id, 'subject'],
                recordstats['change'].ix[patient_id, 'treat_item'],
                recordstats['change'].ix[patient_id, 'access'],
                recordstats['change'].ix[patient_id, 'dmachine'],
                recordstats['change'].ix[patient_id, 'cmachine'],
                recordstats['change'].ix[patient_id, 'reuse'],
                recordstats['change'].ix[patient_id, 'anti_scope'],
                recordstats['change'].ix[patient_id, 'anti'],
                recordstats['change'].ix[patient_id, 'protamine'],
                recordstats['mean'].ix[patient_id, 'target_time'], recordstats['var'].ix[patient_id, 'target_time'],
                recordstats['range'].ix[patient_id, 'target_time'], recordstats['change'].ix[patient_id, 'target_time'],
                recordstats['mean'].ix[patient_id, 'actual_time'], recordstats['var'].ix[patient_id, 'actual_time'],
                recordstats['range'].ix[patient_id, 'actual_time'], recordstats['change'].ix[patient_id, 'actual_time'],
                recordstats['change'].ix[patient_id, 'rway'],
                recordstats['mean'].ix[patient_id, 'ramount'], recordstats['var'].ix[patient_id, 'ramount'],
                recordstats['range'].ix[patient_id, 'ramount'], recordstats['change'].ix[patient_id, 'ramount'],
                recordstats['change'].ix[patient_id, 'ca'],
                recordstats['change'].ix[patient_id, 'k'],
                recordstats['mean'].ix[patient_id, 'dry_w'], recordstats['var'].ix[patient_id, 'dry_w'],
                recordstats['range'].ix[patient_id, 'dry_w'], recordstats['change'].ix[patient_id, 'dry_w'],
                recordstats['mean'].ix[patient_id, 'pre_w'], recordstats['var'].ix[patient_id, 'pre_w'],
                recordstats['range'].ix[patient_id, 'pre_w'], recordstats['change'].ix[patient_id, 'pre_w'],
                recordstats['mean'].ix[patient_id, 'target_ultra'], recordstats['var'].ix[patient_id, 'target_ultra'],
                recordstats['range'].ix[patient_id, 'target_ultra'], recordstats['change'].ix[patient_id, 'target_ultra'],
                recordstats['change'].ix[patient_id, 'food'],
                recordstats['change'].ix[patient_id, 'fluid'],
                recordstats['mean'].ix[patient_id, 'after_w'], recordstats['var'].ix[patient_id, 'after_w'],
                recordstats['range'].ix[patient_id, 'after_w'], recordstats['change'].ix[patient_id, 'after_w'],
                recordstats['mean'].ix[patient_id, 'actual_ultra'], recordstats['var'].ix[patient_id, 'actual_ultra'],
                recordstats['range'].ix[patient_id, 'actual_ultra'], recordstats['change'].ix[patient_id, 'actual_ultra'],
                recordstats['change'].ix[patient_id, 'bloodpos'],
                recordstats['mean'].ix[patient_id, 'SDUFR'], recordstats['var'].ix[patient_id, 'SDUFR'],
                recordstats['range'].ix[patient_id, 'SDUFR'], recordstats['change'].ix[patient_id, 'SDUFR'],
                recordstats['mean'].ix[patient_id, 'vein_change'], recordstats['var'].ix[patient_id, 'vein_change'],
                recordstats['range'].ix[patient_id, 'vein_change'], recordstats['change'].ix[patient_id, 'vein_change'],
                recordstats['mean'].ix[patient_id, 'membrane_change'], recordstats['var'].ix[patient_id, 'membrane_change'],
                recordstats['range'].ix[patient_id, 'membrane_change'], recordstats['change'].ix[patient_id, 'membrane_change'],
                recordstats['mean'].ix[patient_id, 'bloodf_mean'], recordstats['var'].ix[patient_id, 'bloodf_mean'],
                recordstats['range'].ix[patient_id, 'bloodf_mean'], recordstats['change'].ix[patient_id, 'bloodf_mean'],
                recordstats['mean'].ix[patient_id, 'bloodf_var'], recordstats['var'].ix[patient_id, 'bloodf_var'],
                recordstats['range'].ix[patient_id, 'bloodf_var'], recordstats['change'].ix[patient_id, 'bloodf_var'],
                recordstats['mean'].ix[patient_id, 'bloodf_range'], recordstats['var'].ix[patient_id, 'bloodf_range'],
                recordstats['range'].ix[patient_id, 'bloodf_range'], recordstats['change'].ix[patient_id, 'bloodf_range'],
                recordstats['mean'].ix[patient_id, 'bloodf_change'], recordstats['var'].ix[patient_id, 'bloodf_change'],
                recordstats['range'].ix[patient_id, 'bloodf_change'], recordstats['change'].ix[patient_id, 'bloodf_change'],
                recordstats['mean'].ix[patient_id, 'na_mean'], recordstats['var'].ix[patient_id, 'na_mean'],
                recordstats['range'].ix[patient_id, 'na_mean'], recordstats['change'].ix[patient_id, 'na_mean'],
                recordstats['mean'].ix[patient_id, 'na_var'], recordstats['var'].ix[patient_id, 'na_var'],
                recordstats['range'].ix[patient_id, 'na_var'], recordstats['change'].ix[patient_id, 'na_var'],
                recordstats['mean'].ix[patient_id, 'na_range'], recordstats['var'].ix[patient_id, 'na_range'],
                recordstats['range'].ix[patient_id, 'na_range'], recordstats['change'].ix[patient_id, 'na_range'],
                recordstats['mean'].ix[patient_id, 'na_change'], recordstats['var'].ix[patient_id, 'na_change'],
                recordstats['range'].ix[patient_id, 'na_change'], recordstats['change'].ix[patient_id, 'na_change'],
                recordstats['mean'].ix[patient_id, 't_mean'], recordstats['var'].ix[patient_id, 't_mean'],
                recordstats['range'].ix[patient_id, 't_mean'], recordstats['change'].ix[patient_id, 't_mean'],
                recordstats['mean'].ix[patient_id, 't_var'], recordstats['var'].ix[patient_id, 't_var'],
                recordstats['range'].ix[patient_id, 't_var'], recordstats['change'].ix[patient_id, 't_var'],
                recordstats['mean'].ix[patient_id, 't_range'], recordstats['var'].ix[patient_id, 't_range'],
                recordstats['range'].ix[patient_id, 't_range'], recordstats['change'].ix[patient_id, 't_range'],
                recordstats['mean'].ix[patient_id, 't_change'], recordstats['var'].ix[patient_id, 't_change'],
                recordstats['range'].ix[patient_id, 't_change'], recordstats['change'].ix[patient_id, 't_change'],
                recordstats['mean'].ix[patient_id, 'sbp_mean'], recordstats['var'].ix[patient_id, 'sbp_mean'],
                recordstats['range'].ix[patient_id, 'sbp_mean'], recordstats['change'].ix[patient_id, 'sbp_mean'],
                recordstats['mean'].ix[patient_id, 'sbp_var'], recordstats['var'].ix[patient_id, 'sbp_var'],
                recordstats['range'].ix[patient_id, 'sbp_var'], recordstats['change'].ix[patient_id, 'sbp_var'],
                recordstats['mean'].ix[patient_id, 'sbp_range'], recordstats['var'].ix[patient_id, 'sbp_range'],
                recordstats['range'].ix[patient_id, 'sbp_range'], recordstats['change'].ix[patient_id, 'sbp_range'],
                recordstats['mean'].ix[patient_id, 'sbp_change'], recordstats['var'].ix[patient_id, 'sbp_change'],
                recordstats['range'].ix[patient_id, 'sbp_change'], recordstats['change'].ix[patient_id, 'sbp_change'],
                recordstats['mean'].ix[patient_id, 'dbp_mean'], recordstats['var'].ix[patient_id, 'dbp_mean'],
                recordstats['range'].ix[patient_id, 'dbp_mean'], recordstats['change'].ix[patient_id, 'dbp_mean'],
                recordstats['mean'].ix[patient_id, 'dbp_var'], recordstats['var'].ix[patient_id, 'dbp_var'],
                recordstats['range'].ix[patient_id, 'dbp_var'], recordstats['change'].ix[patient_id, 'dbp_var'],
                recordstats['mean'].ix[patient_id, 'dbp_range'], recordstats['var'].ix[patient_id, 'dbp_range'],
                recordstats['range'].ix[patient_id, 'dbp_range'], recordstats['change'].ix[patient_id, 'dbp_range'],
                recordstats['mean'].ix[patient_id, 'dbp_change'], recordstats['var'].ix[patient_id, 'dbp_change'],
                recordstats['range'].ix[patient_id, 'dbp_change'], recordstats['change'].ix[patient_id, 'dbp_change'],
                recordstats['mean'].ix[patient_id, 'pulse_mean'], recordstats['var'].ix[patient_id, 'pulse_mean'],
                recordstats['range'].ix[patient_id, 'pulse_mean'], recordstats['change'].ix[patient_id, 'pulse_mean'],
                recordstats['mean'].ix[patient_id, 'pulse_var'], recordstats['var'].ix[patient_id, 'pulse_var'],
                recordstats['range'].ix[patient_id, 'pulse_var'], recordstats['change'].ix[patient_id, 'pulse_var'],
                recordstats['mean'].ix[patient_id, 'pulse_range'], recordstats['var'].ix[patient_id, 'pulse_range'],
                recordstats['range'].ix[patient_id, 'pulse_range'], recordstats['range'].ix[patient_id, 'pulse_range'],
                recordstats['mean'].ix[patient_id, 'pulse_change'], recordstats['var'].ix[patient_id, 'pulse_change'],
                recordstats['range'].ix[patient_id, 'pulse_change'], recordstats['change'].ix[patient_id, 'pulse_change'],
                recordstats['mean'].ix[patient_id, 'bre_mean'], recordstats['var'].ix[patient_id, 'bre_mean'],
                recordstats['range'].ix[patient_id, 'bre_mean'], recordstats['change'].ix[patient_id, 'bre_mean'],
                recordstats['mean'].ix[patient_id, 'bre_var'], recordstats['var'].ix[patient_id, 'bre_var'],
                recordstats['range'].ix[patient_id, 'bre_var'], recordstats['change'].ix[patient_id, 'bre_var'],
                recordstats['mean'].ix[patient_id, 'bre_range'], recordstats['var'].ix[patient_id, 'bre_range'],
                recordstats['range'].ix[patient_id, 'bre_range'], recordstats['change'].ix[patient_id, 'bre_range'],
                recordstats['mean'].ix[patient_id, 'bre_change'], recordstats['var'].ix[patient_id, 'bre_change'],
                recordstats['range'].ix[patient_id, 'bre_change'], recordstats['change'].ix[patient_id, 'bre_change']
            ]

        patients.index = range(len(patients))
        patients.to_csv(dataset1, encoding='UTF-8')   # 小数据集保存
        print('save dataset1')

        # 额外处理，数据处理可能出错，中间出现id为0的垃圾数据，很可能是前面步骤有错误
        # dataset1 = r'analysis_data/dataset1.csv'
        # dataset1 = pd.read_csv(dataset1, index_col=['patient_id'], encoding='UTF-8')
        # dataset1 = dataset1[dataset1.index != 0]
        # dataset1.to_csv(r'analysis_data/dataset1.csv', encoding='UTF-8')

        # patients = patients[patients['patient_id'] != 0]
        # patients.to_csv(patient_file, encoding='UTF-8')
        print('dataset1 has done')
        
        
    
    
     def build_dataset2(self):
        """
        构建大数据集
        :return:
        """
        patient_file = r'cleaned/cleaned/patient.csv'
        # patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0],
        #                        parse_dates=['begin_date', 'end_date', 'center_begin_date', 'tx_begin_date', 'eventdate',
        #                                     'vascular_access_build_date', 'birth', 'dateSt', 'dateEn', 'deathdate', 'dateHD'])
        patients = pd.read_csv(patient_file, encoding='UTF-8', index_col=[0])
        print('Total lines: %d' % len(patients))
        # del patients['case_no']; del patients['begin_date']; del patients['end_date']; del patients['in_diagnosis']
        # del patients['center_begin_date']; del patients['tx_begin_date']; del patients['begin_unit']; del patients['vascular_access_type']
        # del patients['vascular_access_build_date']; del patients['ID']; del patients['birth']; del patients['dateSt']
        # del patients['dateEn']; del patients['age']; del patients['education']; del patients['deathdate']; del patients['eventdate']
        # del patients['dateHD']; del patients['accessC']; del patients['dialysis']; del patients['HBVDNA']
        # del patients['antiRAAS']; del patients['ACEIandARB'];del patients[u'\u03b1\u03b2blockers']; del patients['ARBdiuretic']
        # del patients['Pbinder']; del patients['CVD']
        # 不是0、1、3、4，而是0、1、2、3
        patients['marital'] = patients['marital'].map({0: 0, 1: 1, 3: 2, 4: 3})

        print(len(patients.columns))
        for col in patients.columns:
            print(col, patients[col].dtype, *list(patients[col].unique()))

        record_file = r'analysis_data/recorditem.csv'
        records = pd.read_csv(record_file, encoding='UTF-8', low_memory=False, index_col=[0],
                              parse_dates=['tx_date', 'target_treat_time', 'actual_treat_time'])
        print('Total lines: %d' % len(records))
        # 删除分类变量
        del records['vein_mean'];
        del records['vein_var'];
        del records['vein_range']
        del records['membrane_mean'];
        del records['membrane_var'];
        del records['membrane_range']
        print(len(records.columns))
        print(records.columns)
        for index, col in enumerate(records.columns):
            print(index+1, col, records[col].dtype, *(list(records[col].unique())[: 10]))

        records['tx_id'] = records.index
        records.index = records['tx_date']

        records['vascular_access_type'] = records['vascular_access_type'].map({
            'AVF': 0, 'SCVC': 1, 'puncture': 2, 'LCVC': 3, 'AVG': 4
        })
        records['dialysis_machine'] = records['dialysis_machine'].map({
            'FSYS': 0, 'BT': 1, 'TL': 2, 'JB': 3, 'BL': 4
        })
        records['clean_machine'] = (records['clean_machine'] == '[>1.5]').astype(int)
        records['ca_concentration'] = records['ca_concentration'].map({
            '[1.25]': 0, '[1.5]': 1, '[1.75]': 2
        })
        records['k_concentration'] = (records['k_concentration'] == '[>=3.0]').astype(int)
        records['target_treat_time'] = (records['target_treat_time'] - pd.to_datetime('1900-01-01')).map(lambda x: x.seconds / 3600.0)
        records['actual_treat_time'] = (records['actual_treat_time'] - pd.to_datetime('1900-01-01')).map(lambda x: x.seconds / 3600.0)

        dates = pd.read_csv(r'cleaned/cleaned/patient_date.csv', index_col=[0], encoding='UTF-8',
                            parse_dates=['deathdate', 'eventdate'])
        dates = dates[['patient_id', 'deathdate', 'eventdate']]
        patients = pd.merge(left=patients, right=dates, on='patient_id')

        dataset2 = r'analysis_data/dataset2.csv'
        records = pd.merge(left=records, right=patients, on='patient_id')
        print(records['survivaltime1'].head())
        records['survivaltime1'] = (records['deathdate'] - records['tx_date']).map(lambda x: x.days / 365.0 * 12)
        print(records['survivaltime1'].head())

        number_columns = ['target_treat_time', 'actual_treat_time', 'replace_amount', 'dry_weight', 'pre_weight',
                          'target_ultrafiltration', 'after_weight', 'actual_ultrafiltration', 'SDUFR_y',
                          'vein_change', 'membrane_change', 'bloodf_mean', 'bloodf_var', 'bloodf_range', 'bloodf_change',
                          'na_mean', 'na_var', 'na_range', 'na_change', 'temperatrue_mean', 'temperatrue_var',
                          'temperatrue_range', 'temperatrue_change', 'sbp_mean', 'sbp_var', 'sbp_range', 'sbp_change',
                          'dbp_mean', 'dbp_var', 'dbp_range', 'dbp_change', 'pulse_mean', 'pulse_var', 'pulse_range',
                          'pulse_change', 'breathe_mean', 'breathe_var', 'breathe_range', 'breathe_change']
        # classify_columns = ['subject', 'treat_item', 'vascular_access_type', 'dialysis_machine', 'clean_machine',
        #                     'reuse_times', 'anticoagulation_scope', 'anticoagulation', 'protamine', 'replacement_way',
        #                     'ca_concentration', 'k_concentration', 'take_food', 'fluid_infusion', 'blood_pressure_pos']
        classify_columns = ['subject', 'treat_item', 'vascular_access_type', 'dialysis_machine', 'clean_machine',
                            'anticoagulation_scope', 'anticoagulation', 'protamine', 'replacement_way',
                            'ca_concentration', 'k_concentration', 'take_food', 'fluid_infusion', 'blood_pressure_pos']
        patientrecordgroup = records.groupby('patient_id', group_keys=False)

        def init_dataset2(dataframe):
            dataframe = pd.DataFrame(dataframe)
            dataframe['seq'] = range(1, len(dataframe) + 1)
            # 数值变量
            for col in number_columns:
                dataframe[col + '_v'] = dataframe[col].copy().diff().fillna(0)
            # 分类变量
            for col in classify_columns:
                temp = dataframe[col].copy().diff().fillna(0)
                temp[temp != 0] = 1
                dataframe[col + '_c'] = temp
            return dataframe

        patientrecordstats = patientrecordgroup.apply(init_dataset2)
        print(len(patientrecordstats.columns))
        patientrecordstats = patientrecordstats[
            (patientrecordstats['tx_date'] >= pd.to_datetime('2009-01-01')) & (patientrecordstats['tx_date'] <= pd.to_datetime('2014-12-31'))]

        patientrecordstats['survivaltime1'] = (patientrecordstats['deathdate'] - patientrecordstats['tx_date']).map(lambda x: x.days / 365.0 * 12)
        patientrecordstats['survivaltime2'] = (patientrecordstats['eventdate'] - patientrecordstats['tx_date']).map(lambda x: x.days / 365.0 * 12)
        del patientrecordstats['deathdate']
        del patientrecordstats['eventdate']
        print(len(patientrecordstats.columns))


        patientrecordstats.to_csv(dataset2, encoding='UTF-8')  # 大数据集保存
        print('dataset2 has done.')