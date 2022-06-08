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
    sex = base_info['sex']

    bmr = calculate_bmr(weight, height, age, sex=sex)
    tef = bmr * 0.1  # 消化食物消耗(估计)
    tdee = bmr + tef + eee + neat

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

    plan_detail = {'fat': round(fat_weight), 'protein': round(protein_weight, 2), 'carbohydrate': round(carbohydrate_weight, 2), 'heat': round(tdee, 2)}
    print(f'[计划]: {plan_detail}')
    return plan_detail


def food_combination(food_lst):
    """
    per 100g
    """
    food_heat = list(map(calculate_food_heat, food_lst))
    sum_heat = sum_food_heat(food_heat)
    plan_heat = calculate_nutrient_intake(_base, 0)
    gap_from_plan(sum_heat, plan_heat)


def calculate_food_heat(name_amount):
    """
    :param food_dic 食物的营养成分表
    :param amount 食物的量(g)
    """
    food_dic, amount = name_amount
    amount_normalized = amount / 100
    fat = food_dic['fat'] * amount_normalized
    protein = food_dic['protein'] * amount_normalized
    carbohydrate = food_dic['carbohydrate'] * amount_normalized
    heat = food_dic['heat'] * amount_normalized

    return {'fat': round(fat, 2), 'protein': round(protein, 2), 'carbohydrate': round(carbohydrate, 2), 'heat': round(heat, 2)}


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
    for k, v in sum_heat.items():
        sum_heat[k] = round(v, 2)
    print(f'[当前]: {sum_heat}')
    return sum_heat


def gap_from_plan(current, plan):
    """
    当前热量与计划热量的差距
    """
    gap = {'fat': 0, 'protein': 0, 'carbohydrate': 0, 'heat': 0}
    for k, v in current.items():
        gap[k] = round(v - plan[k], 2)

    print(f'[差值]: {gap}')


def grid_search(food_lst, plan_intake):
    """
    网格搜索所有组合
    :param food_lst:
    :param plan_intake:
    :return:
    """



def select_food():
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
    danish_pastry = {'fat': 25.2, 'protein': 7.1, 'carbohydrate': 45.7, 'heat': 430}  # 丹麦酥
    sweet_potato = {'fat': 0.1, 'protein': 1.6, 'carbohydrate': 20.1, 'heat': 86}  # 红薯
    brown_rice = {'fat': 2.4, 'protein': 9, 'carbohydrate': 73.5, 'heat': kj2kcal(1523)}  # 糙米

    day1 = [(beef_1, 150), (shrimp, 144), (oatmeal, 70), (rice, 300), (oat_milk, 270), (egg, 150),
                  (banana, 70), (sunflower_seed_oil, 10), (danish_pastry, 80)]

    day2 = [(salmon, 200), (shrimp, 144), (danish_pastry, 80), (oat_milk, 150), (rice, 200), (sweet_potato, 150),
            (egg, 120), (oatmeal, 60), (banana, 140), (brown_rice, 40)]

    food_combination(day2)






if __name__ == '__main__':
    """
    营养素摄入量为规律健身建议值，若活动较少应当减少蛋白质摄入量
    eee 每日运动消耗，一小时运动250左右
    neat 除运动外每日活动消耗, 上班族300左右
    """
    wll = {'sex': 'female', 'weight': 54.5, 'height': 166.5, 'age': 26, 'eee': 0, 'neat': 200}
    _base = {'sex': 'male', 'weight': 74, 'height': 188, 'age': 28, 'eee': 0, 'neat': 300}
    select_food()
