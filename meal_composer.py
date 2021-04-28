import random
import json

def load_json_from_file():
    with open('json/zupy.json', 'r', encoding='utf-8') as f_json:
        data = json.load(f_json)
        for value in data.values():
            print(value)


def make_daily_menu(recipes, kcal_limit, meals_limit):
    kcal_daily = 0
    protein_daily = 0
    carbs_daily = 0
    fat_daily = 0
    limit = 1

    while kcal_limit >= kcal_daily:
        random_recipe = random.randint(1, len(recipes))
        if kcal_daily + float(recipes[random_recipe]['kcal']) > kcal_limit:
            break
        kcal_daily += float(recipes[random_recipe]['kcal'])
        protein_daily += float(recipes[random_recipe]['b'])
        carbs_daily += float(recipes[random_recipe]['ww'])
        fat_daily += float(recipes[random_recipe]['t'])

        print(recipes[random_recipe]['nazwa'])
        print(f'kcal: {kcal_daily} | b: {protein_daily} | ww: {carbs_daily} | t: {fat_daily}')
        limit += 1

load_json_from_file()