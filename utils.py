# _*_ coding: utf-8 _*_
# @Time : 2022/6/7 10:11 
# @Author : lxf 
# @Version：V 0.1
# @File : utils.py
# @desc :
import pandas as pd


def kj2kcal(kj):
    """
    千焦转千卡
    :param kj:
    :return:
    """
    return kj * 0.2389


def kcal2kj(kcal):
    """
    千卡转千焦
    :param kcal:
    :return:
    """
    return kcal / 0.2389


def dicts2df(dict_lst):
    """
    将一组dict转为dataframe
    """
    merged_dict = {}
    for d in dict_lst:
        if not merged_dict:
            merged_dict = dict(zip(d.keys(), [[] for x in range(len(d))]))
        for k, v in d.items():
            merged_dict[k].append(v)

    merged_df = pd.DataFrame(merged_dict)

    return merged_df
