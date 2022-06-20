# _*_ coding: utf-8 _*_
# @Time : 2022/6/8 23:01
# @Author : lxf
# @Version：V 0.1
# @File : main.py
# @desc :

from tools.utils import kj2kcal, grid_search


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

    plan_detail = {'fat': round(fat_weight), 'protein': round(protein_weight, 2), 'carbohydrate': round(carbohydrate_weight, 2), 'kcal': round(tdee, 2)}
    print(f'[计划]: {plan_detail}')
    return plan_detail


def food_combination(food_lst, base_info):
    """
    per 100g
    """
    food_heat = list(map(calculate_food_heat, food_lst))
    sum_heat = sum_food_heat(food_heat)
    plan_heat = calculate_nutrient_intake(base_info, 0)
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
    heat = food_dic['kcal'] * amount_normalized

    return {'fat': round(fat, 2), 'protein': round(protein, 2), 'carbohydrate': round(carbohydrate, 2), 'kcal': round(heat, 2)}


def sum_food_heat(food_heat_lst):
    """
    多种实物各营养素求和
    """
    sum_heat = {'fat': 0, 'protein': 0, 'carbohydrate': 0, 'kcal': 0}
    for food in food_heat_lst:
        sum_heat['fat'] += food['fat']
        sum_heat['protein'] += food['protein']
        sum_heat['carbohydrate'] += food['carbohydrate']
        sum_heat['kcal'] += food['kcal']
    for k, v in sum_heat.items():
        sum_heat[k] = round(v, 2)
    print(f'[当前]: {sum_heat}')
    return sum_heat


def gap_from_plan(current, plan):
    """
    当前热量与计划热量的差距
    """
    gap = {'fat': 0, 'protein': 0, 'carbohydrate': 0, 'kcal': 0}
    for k, v in current.items():
        gap[k] = round(v - plan[k], 2)

    print(f'[差值]: {gap}')


def select_food():
    beef_1 = {'fat': 22.3, 'protein': 16.9, 'carbohydrate': 4.1, 'kcal': kj2kcal(1182), 'food_name': '山姆牛肉饼', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 75}  # 山姆牛肉饼
    beef_2 = {'fat': 1.8, 'protein': 19.2, 'carbohydrate': 2.9, 'kcal': 105, 'food_name': '牛腿肉', 'food_id': '', 'dietary_fiber': 0, 'sodium': 79.9, 'price': '', 'desc': '', 'g_step': 50}  # 牛腿肉
    shrimp = {'fat': 0.8, 'protein': 18.6, 'carbohydrate': 2.8, 'kcal': 45, 'food_name': '去皮对虾', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 15}  # 虾仁
    oatmeal = {'fat': 15.8, 'protein': 7.4, 'carbohydrate': 63.2, 'kcal': kj2kcal(1857), 'food_name': '水果麦片', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 10}  # 水果麦片
    oatmeal_2 = {'fat': 9.3, 'protein': 11, 'carbohydrate': 60.5, 'kcal': kj2kcal(1656), 'food_name': '麦片', 'food_id': '', 'dietary_fiber': 12, 'sodium': 8, 'price': '', 'desc': '', 'g_step': 10}  # 麦片
    rice = {'fat': 0.9, 'protein': 7.9, 'carbohydrate': 77.2, 'kcal': 346, 'food_name': '生米', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 10}  # 生米
    oat_milk = {'fat': 0.8, 'protein': 1, 'carbohydrate': 8.1, 'kcal': 45, 'food_name': '燕麦牛奶', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 10}  # 燕麦牛奶
    egg = {'fat': 9, 'protein': 12.7, 'carbohydrate': 1.5, 'kcal': 138, 'food_name': '鸡蛋', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 40}  # 鸡蛋
    mix_nut_1 = {'fat': 50.7, 'protein': 19, 'carbohydrate': 14.3, 'kcal': kj2kcal(2442), 'food_name': '山姆混合坚果', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 10}  # 山姆混合坚果
    mix_nut_2 = {'fat': 10.4/26*100, 'protein': 3.5/26*100, 'carbohydrate': 8.2/26*100, 'kcal': kj2kcal(597/26*100), 'food_name': '每日坚果', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 26}  # 每日坚果
    banana = {'fat': 0.2, 'protein': 1.4, 'carbohydrate': 22, 'kcal': 93, 'food_name': '香蕉', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 70}  #
    sunflower_seed_oil = {'fat': 100, 'protein': 0, 'carbohydrate': 0, 'kcal': 899, 'food_name': '葵花籽油', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 5}  # 葵花籽油
    salmon = {'fat': 21.6, 'protein': 17.8, 'carbohydrate': 0, 'kcal': 263, 'food_name': '三文鱼块', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 100}  # 三文鱼块
    danish_pastry = {'fat': 25.2, 'protein': 7.1, 'carbohydrate': 45.7, 'kcal': 430, 'food_name': '丹麦酥', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 80}  # 丹麦酥
    sweet_potato = {'fat': 0.1, 'protein': 1.6, 'carbohydrate': 20.1, 'kcal': 86, 'food_name': '红薯', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 20}  # 红薯
    brown_rice = {'fat': 2.4, 'protein': 9, 'carbohydrate': 73.5, 'kcal': kj2kcal(1523), 'food_name': '糙米', 'food_id': '', 'dietary_fiber': '', 'sodium': '', 'price': '', 'desc': '', 'g_step': 10}  # 糙米
    mantou = {'fat': 2.8, 'protein': 8.7, 'carbohydrate': 50, 'kcal': kj2kcal(1101), 'food_name': '牛乳小馒头', 'food_id': '', 'dietary_fiber': '', 'sodium': 34, 'price': '', 'desc': '', 'g_step': 30}  # 馒头
    coffee = {'fat': 3, 'protein': 2.9, 'carbohydrate': 6.5, 'kcal': 65, 'food_name': '拿铁', 'food_id': '', 'dietary_fiber': '', 'sodium': 51, 'price': '', 'desc': '', 'g_step': 100}  # 馒头
    cherry = {'fat': 0.2, 'protein': 1.1, 'carbohydrate': 10.2, 'kcal': 46, 'food_name': '樱桃', 'food_id': '', 'dietary_fiber': '', 'sodium': 8, 'price': '', 'desc': '', 'g_step': 50}  # 馒头
    beef_3 = {'fat': 13.5, 'protein': 13.2, 'carbohydrate': 1.9, 'kcal': 184, 'food_name': '肥牛', 'food_id': '', 'dietary_fiber': '', 'sodium': 195, 'price': '', 'desc': '', 'g_step': 100}  # 馒头
    xilanhua = {'fat': 0.6, 'protein': 3.5, 'carbohydrate': 3.7, 'kcal': 27, 'food_name': '西蓝花', 'food_id': '', 'dietary_fiber': '', 'sodium': 0, 'price': '', 'desc': '', 'g_step': 0}  # 西蓝花
    qingjiao = {'fat': 0.3, 'protein': 0.8, 'carbohydrate': 5.2, 'kcal': 22, 'food_name': '青椒', 'food_id': '', 'dietary_fiber': '', 'sodium': 0, 'price': '', 'desc': '', 'g_step': 0}  # 青椒
    hongshu = {'fat': 0.1, 'protein': 1.6, 'carbohydrate': 20.1, 'kcal': 22, 'food_name': '红薯', 'food_id': '', 'dietary_fiber': '', 'sodium': 55, 'price': '', 'desc': '', 'g_step': 0}  # 红薯
    qiukui = {'fat': 0.2, 'protein': 1.8, 'carbohydrate': 6.2, 'kcal': 25, 'food_name': '秋葵', 'food_id': '', 'dietary_fiber': 1.8, 'sodium': 8.7, 'price': '', 'desc': '', 'g_step': 100}  # 秋葵
    nfc = {'fat': 0, 'protein': 0.6, 'carbohydrate': 10, 'kcal': kj2kcal(205), 'food_name': 'nfc橙汁', 'food_id': '', 'dietary_fiber': 0, 'sodium': 0, 'price': '', 'desc': '', 'g_step': 300}  # nfc橙汁
    apple = {'fat': 0.2, 'protein': 0.4, 'carbohydrate': 13.7, 'kcal': 53, 'food_name': '苹果', 'food_id': '', 'dietary_fiber': 1.7, 'sodium': 1.3, 'price': '', 'desc': '', 'g_step': 300}  # 苹果
    chicken_breast = {'fat': 1.9, 'protein': 24.6, 'carbohydrate': 0.6, 'kcal': 118, 'food_name': '鸡胸肉', 'food_id': '', 'dietary_fiber': 0, 'sodium': 44.8, 'price': '', 'desc': '', 'g_step': 300}
    niushe = {'fat': 13.3, 'protein': 17, 'carbohydrate': 2, 'kcal': 196, 'food_name': '牛舌', 'food_id': '', 'dietary_fiber': 0, 'sodium': 58.4, 'price': '', 'desc': '', 'g_step': 300}
    niuyouguo = {'fat': 100, 'protein': 0, 'carbohydrate': 0, 'kcal': 884, 'food_name': '牛油果', 'food_id': '', 'dietary_fiber': 0, 'sodium': 0, 'price': '', 'desc': '', 'g_step': 300}
    beijibei = {'fat': 1.1, 'protein': 11.1, 'carbohydrate': 3.8, 'kcal': 73, 'food_name': '北极贝', 'food_id': '', 'dietary_fiber': 0, 'sodium': 250, 'price': '', 'desc': '', 'g_step': 300}
    bread1 = {'fat': 13.5, 'protein': 8.3, 'carbohydrate': 51.8, 'kcal': 73, 'food_name': '叮咚经典原味北海道吐司面包', 'food_id': '', 'dietary_fiber': 0, 'sodium': 247, 'price': '', 'desc': '', 'g_step': 300}


    # day1 = [(beef_1, 150), (shrimp, 144), (oatmeal, 70), (rice, 300), (oat_milk, 270), (egg, 150),
    #               (banana, 70), (sunflower_seed_oil, 10), (danish_pastry, 80)]
    #
    # day2 = [(salmon, 200), (shrimp, 144), (danish_pastry, 160), (oat_milk, 150), (rice, 200), (sweet_potato, 150),
    #         (egg, 100), (oatmeal, 60), (banana, 140), (brown_rice, 40)]

    # day3 = [(beef_2, 150), (shrimp, 80), (salmon, 100), (danish_pastry, 80), (oat_milk, 250), (rice, 140), (sweet_potato, 235),
    #         (egg, 80), (oatmeal, 60), (banana, 0), (brown_rice, 50), (mantou, 90), (mix_nut_2, 26)]

    # day4 = [(beef_3, 200), (cherry, 150), (coffee, 360), (beef_2, 180), (rice, 80), (oatmeal, 60), (banana, 70), (brown_rice, 40), (mantou, 90), (mix_nut_2, 26)]

    # day7 = [(beef_2, 150), (mantou, 120), (rice, 250), (oatmeal, 60), (banana, 60), (xilanhua, 140), (qingjiao, 130),
    #         (oat_milk, 350), (salmon, 100), (mix_nut_2, 26), (shrimp, 80)]
    #
    # day8 = [(beef_2, 130), (mantou, 90), (rice, 140), (brown_rice, 60), (oatmeal, 70), (banana, 60), (qingjiao, 150),
    #         (oat_milk, 400), (salmon, 200), (mix_nut_2, 26), (hongshu, 240), (egg, 80)]
    #
    # day9 = [(beef_2, 130), (mantou, 90), (rice, 140), (brown_rice, 60), (oatmeal, 70), (banana, 60), (qingjiao, 150),
    #         (oat_milk, 400), (salmon, 200), (mix_nut_2, 26), (hongshu, 240), (egg, 80)]

    # day10 = [(beef_2, 150), (mantou, 90), (rice, 150), (brown_rice, 60), (oatmeal, 40),
    #         (oat_milk, 400), (mix_nut_2, 26), (xilanhua, 40), (nfc, 300), (qiukui, 170), (shrimp, 110), (sunflower_seed_oil, 15)]

    day13 = [(beef_2, 190), (rice, 230), (oatmeal, 30), (oat_milk, 300), (xilanhua, 230), (sunflower_seed_oil, 15),
             (chicken_breast, 170), (bread1, 30)]

    # grid_search(day3, calculate_nutrient_intake(lxf, 0))
    food_combination(day13, lxf)







if __name__ == '__main__':
    """
    营养素摄入量为规律健身建议值，若活动较少应当减少蛋白质摄入量
    eee 每日运动消耗，一小时运动250左右
    neat 除运动外每日活动消耗, 上班族300左右
    """
    lele = {'sex': 'female', 'weight': 53.5, 'height': 166.5, 'age': 26, 'eee': 0, 'neat': 200}
    lxf = {'sex': 'male', 'weight': 74, 'height': 188, 'age': 28, 'eee': 0, 'neat': 300}
    select_food()
