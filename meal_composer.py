import random
import json
import os
from parameters import *

def load_json_from_file():
    with open(f'json/{JSON_DB_NAME}', 'r', encoding='utf-8') as f_json:
        if os.stat(f'json/{JSON_DB_NAME}').st_size > 0:
            recipes = json.load(f_json)
            print(f'Wczytano plik z przepisami. Ilość przepisów w bazie to: {len(recipes)} ')
            print("-----------------------------------------------------------")
            print("-----------------------------------------------------------")
            return recipes
        else:
            print('Plik z przepisami jest pusty !')

def print_all_recipes(test):
    for value in test:
        print(value)

def random_meal(recipes, meal_type):
    filtered_recipes = []
    for k, v in recipes.items():
        for k1, v1 in v.items():
            if v1 == meal_type:
                filtered_recipes.append(k)
    return random.choice(filtered_recipes)

def daily_menu(recipes, tollerance=100, kcal_limit=1500, meals_limit=3):
    daily_kcal, total_kcal, total_proteins, total_fat, total_carbs, i = 0, 0, 0, 0, 0, 0
    kcal_tolerance = tollerance
    daily_meal_set, meal_list = [], []

    if recipes is not None:
        if meals_limit > 5 or meals_limit < 3:
            print('Wybierz liczbę posiłków z przedziału: 3 - 5')
        if meals_limit == 3:
            meal_list = ['sniadania-kolacje', 'dania-glowne', 'sniadania-kolacje']
        if meals_limit == 4:
            meal_list = ['sniadania-kolacje', 'sniadania-kolacje', 'dania-glowne', 'sniadania-kolacje']
        if meals_limit == 5:
            meal_list = ['sniadania-kolacje', 'sniadania-kolacje', 'dania-glowne', 'przekaski', 'sniadania-kolacje']

        while (kcal_limit - kcal_tolerance >= daily_kcal) or (kcal_limit + kcal_tolerance  <= daily_kcal):
            daily_meal_set.clear()
            daily_kcal = 0

            for meal_type in meal_list:
                meal = random_meal(recipes, meal_type)
                daily_meal_set.append(meal)
                daily_kcal += int(float(recipes[meal]['kcal']))

            if i == ITERATION_LIMITER:
                print("Nie udało się dobrać kaloryczności. Spróbuj zwiększyć liczbę posiłków lub zmniejsz limit kalorii.")
                daily_meal_set.clear()
                daily_kcal = 0
                break
            i += 1

    if daily_kcal != 0:
        print(f'Menu wybrane dla limitu kcal: {kcal_limit} i {meals_limit} posiłków to: ')
        print("***********************************************************")

    for index, meal in enumerate(daily_meal_set):
        meal_kcal = int(float(recipes[meal]['kcal']))
        meal_protein = int(float(recipes[meal]['b']))
        meal_fat = int(float(recipes[meal]['t']))
        meal_carbs = int(float(recipes[meal]['ww']))

        total_kcal += meal_kcal
        total_proteins += meal_protein
        total_fat += meal_fat
        total_carbs += meal_carbs

        url = recipes[meal]['url']

        print(f"Posiłek nr: {index+1} | {recipes[meal]['nazwa']}")
        print(f"Wartość odżywcza: kcal: {meal_kcal} | b: {meal_protein} | t: {meal_fat} | ww: {meal_carbs}")
        print(f"URL: {url}")
        print("***********************************************************")
    if daily_kcal != 0:
        print(f'Podsumowanie: kcal: {total_kcal} | b: {total_proteins} | t: {total_fat} | ww: {total_carbs}')


if __name__ == "__main__":
    all_meals = load_json_from_file()
    daily_menu(all_meals, 100, 2300, 5)