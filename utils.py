# _*_ coding: utf-8 _*_
# @Time : 2022/6/7 10:11 
# @Author : lxf 
# @Version：V 0.1
# @File : utils.py
# @desc :
import numpy as np
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


def weighted_mse(current, plan, weight=None):
    """
    带权值的mse
    :param current:  当前摄入量
    :param plan:  计划摄入量
    :param weight: 三种营养素的惩罚权值
    :return:
    """
    if not weight:
        weight = [1 for x in range(len(current))]
    mse_test = np.sum(((current - plan) * weight) ** 2) / len(plan)

    return mse_test


def grid_search(food_lst, plan_intake):
    """
    网格搜索所有组合
    :param food_lst:
    :param plan_intake:
    :return:
    """
    plan_fat = plan_intake['fat']
    plan_protein = plan_intake['protein']
    plan_carbohydrate = plan_intake['carbohydrate']
    plan_kcal = plan_intake['kcal']

    food_grid = []  # 每种食物网格搜索的范围
    for food in food_lst:
        _range = [range(0, int(plan_kcal/food['kcal']), food.get('g_step', 20))]
        food_grid.append(_range)

    print(food_grid)


def calculate_best_plan():
    return


if __name__ == '__main__':
    a = np.array([9, 8, 7])
    b = np.array([6, 9, 3])
    c = np.array([2, 1, 1])
    print(a-b)
    print((a-b)*c)
