# _*_ coding: utf-8 _*_
# @Time : 2022/6/7 17:03 
# @Author : lxf 
# @Version：V 0.1
# @File : db_op.py
# @desc :
import pandas as pd
from config.path import DB_PATH
from utils import dicts2df


def insert_csv(info_df):
    """
    将改动写入csv中
    :param info_df:
    :return:
    """
    df = pd.read_csv(DB_PATH)


def search(k, v):
    """
    查询csv中内容
    :param k:
    :param v:
    :return:
    """