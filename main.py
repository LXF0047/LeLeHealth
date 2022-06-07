# _*_ coding: utf-8 _*_
# @Time : 2022/6/8 23:01
# @Author : lxf
# @Version：V 0.1
# @File : main.py
# @desc :
from utils import kj2kcal


def calculate_bmr(weight, height, age, sex='male'):
    """
    calculate bmr using revised Harris-Benedict formula
    :param weight kg
    :param height cm
    :param age year
    :param sex 'male'/'female'
    """
    if sex == 'male':
        bmr = 13.379*weight+4.799*height+5.677*age+88.362
    else:
        bmr = 9.247*weight+3.098*height+4.33*age+447.593
    return bmr


def calculate_tdee(base_info):
    """
    calculate Total Daily Energy Expenditure
    """
    weight = base_info['weight']
    height = base_info['height']
    age = base_info['age']
    eee = base_info['eee']
    neat = base_info['neat']

    bmr = calculate_bmr(weight, height, age, sex='male')
    tef = bmr * 0.1  # 消化食物消耗(估计)
    tdee = bmr + tef + eee + neat
    print(f'每日消耗量: {tdee}')

    return tdee


def calculate_nutrient_intake(base_info, deficit):
    """
    :param deficit 目标热量差值
    :param base_info
    """
    if deficit < 0:
        # 减脂
        fat_coefficient = 0.35
        protein_coefficient = 2
    else:
        # 增肌
        fat_coefficient = 0.25
        protein_coefficient = 1.6
    tdee = calculate_tdee(base_info)
    weight = base_info['weight']

    fat_heat = fat_coefficient * tdee
    protein_weight = protein_coefficient * weight
    protein_heat = protein_weight * 4
    carbohydrate_heat = tdee - (fat_heat + protein_heat) + deficit

    fat_weight = fat_heat / 9
    carbohydrate_weight = carbohydrate_heat / 4

    print(f'脂肪摄入:{round(fat_weight)}g, 蛋白质摄入: {round(protein_weight)}g, 碳水摄入: {round(carbohydrate_weight)}g')


def food_combination():
    """
    per 100g
    """
    beef_1 = {'fat': 22.3, 'protein': 16.9, 'carbohydrate': 4.1, 'heat': kj2kcal(1182)}  # 山姆牛肉饼
    shrimp = {'fat': 0.8, 'protein': 18.6, 'carbohydrate': 2.8, 'heat': 45}  # 虾仁
    oatmeal = {'fat': 15.8, 'protein': 7.4, 'carbohydrate': 63.2, 'heat': kj2kcal(1857)}  # 水果麦片
    rice = {'fat': 0.9, 'protein': 7.9, 'carbohydrate': 77.2, 'heat': 346}  # 生米
    oat_milk = {'fat': 0.8, 'protein': 1, 'carbohydrate': 8.1, 'heat': 45}  # 燕麦牛奶
    egg = {'fat': 9, 'protein': 12.7, 'carbohydrate': 1.5, 'heat': 138}  # 鸡蛋
    mix_nut_1 = {'fat': 50.7, 'protein': 19, 'carbohydrate': 14.3, 'heat': kj2kcal(2442)}  # 山姆混合坚果
    mix_nut_2 = {'fat': 10.4/26*100, 'protein': 3.5/26*100, 'carbohydrate': 8.2/26*100, 'heat': kj2kcal(597/26*100)}  # 每日坚果
    banana = {'fat': 0.2, 'protein': 1.4, 'carbohydrate': 22, 'heat': 93}  #
    sunflower_seed_oil = {'fat': 100, 'protein': 0, 'carbohydrate': 0, 'heat': 899}  # 葵花籽油
    salmon = {'fat': 21.6, 'protein': 17.8, 'carbohydrate': 0, 'heat': 263}  # 三文鱼块

    beef_1_heat = calculate_food_heat(beef_1, 150)
    oatmeal_heat = calculate_food_heat(oatmeal, 70)
    shrimp_heat = calculate_food_heat(shrimp, 144)
    rice_heat = calculate_food_heat(rice, 300)
    oat_milk_heat = calculate_food_heat(oat_milk, 270)
    egg_milk_heat = calculate_food_heat(egg, 150)
    mix_nut_2_heat = calculate_food_heat(mix_nut_2, 26)
    banana_heat = calculate_food_heat(banana, 350)
    salmon_heat = calculate_food_heat(salmon, 100)
    # sunflower_seed_oil_heat = calculate_food_heat(sunflower_seed_oil, 20)

    sum_heat = sum_food_heat([beef_1_heat, oatmeal_heat, shrimp_heat, rice_heat, oat_milk_heat, egg_milk_heat, banana_heat, mix_nut_2_heat])
    plan_heat = {'fat': 74, 'protein': 118, 'carbohydrate': 379, 'heat': 2653}
    gap_from_plan(sum_heat, plan_heat)


def calculate_food_heat(food_dic, amount):
    """
    :param food_dic 食物的营养成分表
    :param amount 食物的量(g)
    """
    amount_normalized = amount / 100
    fat = food_dic['fat'] * amount_normalized
    protein = food_dic['protein'] * amount_normalized
    carbohydrate = food_dic['carbohydrate'] * amount_normalized
    heat = food_dic['heat'] * amount_normalized

    return {'fat': fat, 'protein': protein, 'carbohydrate': carbohydrate, 'heat': heat}


def sum_food_heat(food_heat_lst):
    """
    多种实物各营养素求和
    """
    sum_heat = {'fat': 0, 'protein': 0, 'carbohydrate': 0, 'heat': 0}
    for food in food_heat_lst:
        sum_heat['fat'] += food['fat']
        sum_heat['protein'] += food['protein']
        sum_heat['carbohydrate'] += food['carbohydrate']
        sum_heat['heat'] += food['heat']

    print(f'当前食各营养素含量: {sum_heat}')
    return sum_heat


def gap_from_plan(current, plan):
    """
    当前热量与计划热量的差距
    """
    gap = {'fat': 0, 'protein': 0, 'carbohydrate': 0, 'heat': 0}
    for k, v in current.items():
        gap[k] = v - plan[k]

    print(f'当前各营养素差距: {gap}')



if __name__ == '__main__':
    """
    营养素摄入量为规律健身建议值，若活动较少应当减少蛋白质摄入量
    eee 每日运动消耗，一小时运动250左右
    neat 除运动外每日活动消耗, 上班族300左右
    """
    _base = {'weight': 74, 'height': 188, 'age': 28, 'eee': 0, 'neat': 300}
    calculate_nutrient_intake(_base, 0)
    food_combination()

    # 计划 脂肪摄入:74g, 蛋白质摄入: 118g, 碳水摄入: 379g 每日消耗量: 2653

