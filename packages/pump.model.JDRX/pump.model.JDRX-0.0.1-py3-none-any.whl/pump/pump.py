#!/usr/bin/python35
# coding: utf-8


"""
@version: 1.0
@author: LiYuBao
@contact: LiYuBao@evercreative.com.cn
@site: http://www.evercreative.com.cn/
@software: PyCharm
@file: pump.py
@time: 2019/2/14 15:04
"""


import numpy as np
import pandas as pd
from decimal import Decimal
import json
import pickle


from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.preprocessing import PolynomialFeatures



def dict_to_pd(dict):
    lk = []
    lv = []
    for key in dict:
        lk.append(key)
        lv.append(dict[key])

    a = {'key': lk, 'value': lv}
    df = pd.DataFrame(a)

    return df


def set_precision(num, digit):
    precision_str = '{:.%d' % (digit) + 'f}'
    dec_val = precision_str.format(Decimal(num))
    return float(dec_val)


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def model_train(jsonData, path, id):
    p = Pump(jsonData)
    path_id = ''.join([path, id, '.pk'])
    f = open(path_id, 'wb')
    pickle.dump(p, f)

    return True


class Pump:
    def __init__(self, data):
        self.data = json.loads(data)

        flow_lift = self.data['model_init']['flow_lift']
        flow_power = self.data['model_init']['flow_power']
        freq_flow_lift = self.data['model_init']['freq_flow_lift']
        freq_flow_power = self.data['model_init']['freq_flow_power']

        self.df_flow_lift = dict_to_pd(flow_lift)
        self.df_flow_power = dict_to_pd(flow_power)
        self.df_freq_flow_lift = dict_to_pd(freq_flow_lift)
        self.df_freq_flow_power = dict_to_pd(freq_flow_power)

        self.k = self.data['model_init']['k']['value']
        self.poly = PolynomialFeatures(degree=2)

        def high_model_train(df_train, df_valid, k):
            X_train_poly = self.poly.fit_transform(df_train[['key']])
            y_train = df_train[['value']]

            clf = Ridge()
            clf.fit(X_train_poly, y_train)

            # 使用变频数据对模型校验
            df_predict = clf.predict(self.poly.fit_transform(df_valid[['key']])) * k * k
            df_mape = pd.DataFrame(columns=['true', 'predict'])
            df_mape['true'] = df_valid['value']
            df_mape['predict'] = df_predict
            mape = mean_absolute_percentage_error(df_mape['true'], df_mape['predict'])
            # print(mape)

            return clf

        def power_model_train(df_train, df_valid, k):
            X_train_poly = self.poly.fit_transform(df_train[['key']])
            y_train = df_train[['value']]

            clf = Ridge()
            clf.fit(X_train_poly, y_train)

            # 使用变频数据对模型校验
            df_predict = clf.predict(self.poly.fit_transform(df_valid[['key']])) * k * k * k
            df_mape = pd.DataFrame(columns=['true', 'predict'])
            df_mape['true'] = df_valid['value']
            df_mape['predict'] = df_predict
            mape = mean_absolute_percentage_error(df_mape['true'], df_mape['predict'])

            return clf

        self.high_model = high_model_train(self.df_flow_lift, self.df_freq_flow_lift, self.k)
        self.power_model = power_model_train(self.df_flow_power, self.df_freq_flow_power, self.k)

        self.high_model_coef = self.high_model.coef_[0]
        self.high_model_intercept = self.high_model.intercept_
        self.power_model_coef = self.power_model.coef_[0]
        self.power_model_intercept = self.power_model.intercept_


    # 扬程预测
    def high_predict(self, flow, k):
        flow_poly = self.poly.fit_transform(flow)
        predict = list(self.high_model.predict(flow_poly))
        return set_precision(predict[0][0] * k * k, 2)

    # 功率预测
    def power_predict(self, flow, k):
        flow_poly = self.poly.fit_transform(flow)
        predict = list(self.power_model.predict(flow_poly))
        return set_precision(predict[0][0] * k * k * k, 3)

    # 效率计算
    def get_efficiency(self, flow, high, power):
        power_hat = 1000*9.8*flow/3600*high
        efficiency = power_hat/(1000*power)
        return set_precision(efficiency, 2)


if __name__ == '__main__':
    # df_pump = pd.read_excel('langfang-pump2.xlsx')
    # df_pump_n2 = df_pump[df_pump.pump_no == 2]
    # df_pump_n3 = df_pump[df_pump.pump_no == 3]

    jsonData = '{"model_init": {' \
               '"flow_lift": {"1000": 45,"1500": 40,"2000": 27,"2500": 20,"3000": 14,"3500": 8},' \
               '"flow_power": {"1000": 120,"1500": 180,"2000": 220,"2500": 280},' \
               '"freq_flow_lift": {"1000": 41,"1500": 35,"2000": 24,"2500": 17.8},' \
               '"freq_flow_power": {"1000": 100,"1500": 150,"2000": 200,"2500": 250},' \
               '"k": {"value": 0.95,"low": 0.5,"high": 1},' \
               '"high_efficiency": {"low": 500,"high": 1500}}}'
    #
    # path = 'D:\\study\\code\\gas_predict\\'
    # id = '001'
    # path_id = ''.join([path, id, '.pk'])
    # model_train(jsonData, path, id)
    #
    #
    # f = open(path_id, 'rb')
    # obj = pickle.load(f)
    # hp = obj.high_predict(1200, 0.8)
    # pp = obj.power_predict(1200, 0.8)
    # eff = obj.get_efficiency(1200, 27.19, 120)
    # print(hp, pp, eff)
    # print("-------------------")

