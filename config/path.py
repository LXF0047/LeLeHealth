# _*_ coding: utf-8 _*_
# @Time : 2022/6/7 17:04 
# @Author : lxf 
# @Version：V 0.1
# @File : path.py
# @desc :
import os

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'database', 'food_calorie_chart.csv')
