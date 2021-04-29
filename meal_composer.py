import random
import json


def load_json_from_file():
    with open(f'json/recipes_database.json', 'r', encoding='utf-8') as f_json:
        recipes = json.load(f_json)
        print(f'ilosc przepisów w bazie to: {len(recipes)} ')
        return recipes

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

def daily(recipes, kcal_limit, meals_limit):
    kcal_daily = 0

    while kcal_limit >= kcal_daily:
        if meals_limit == 3:
            meal1 = random_meal(recipes, 'sniadania-kolacje')
            meal2 = random_meal(recipes, 'dania-glowne')
            meal3 = random_meal(recipes, 'sniadania-kolacje')
        elif meals_limit == 4:
            meal1 = random_meal(recipes, 'sniadania-kolacje')
            meal2 = random_meal(recipes, 'sniadania-kolacje')
            meal3 = random_meal(recipes, 'dania-glowne')
            meal4 = random_meal(recipes, 'sniadania-kolacje')
        elif meals_limit == 5:
            meal1 = random_meal(recipes, 'sniadania-kolacje')
            meal2 = random_meal(recipes, 'sniadania-kolacje')
            meal3 = random_meal(recipes, 'dania-glowne')
            meal4 = random_meal(recipes, 'sniadania-kolacje')
            meal5 = random_meal(recipes, 'sniadania-kolacje')


       # kcal_daily += float(recipes[random_recipe]['kcal'])

    print(recipes[meal1]['nazwa'])
    print(recipes[meal2]['nazwa'])
    print(recipes[meal3]['nazwa'])

def make_daily_menu(recipes, kcal_limit, meals_limit):
    kcal_daily = 0
    protein_daily = 0
    carbs_daily = 0
    fat_daily = 0
    tollerance_kcal = 100
    meal_counter = 1

    daily_breakfast = []
    daily_dinner = []
    daily_supper = []

    while kcal_limit >= kcal_daily:
        random_recipe = random.choice(list(recipes))
        if (recipes[random_recipe]['rodzaj'] == 'sniadania-kolacje') and meal_counter <= 2:
            daily_breakfast.append(recipes[random_recipe]['nazwa'])
            meal_counter +=1
        elif ((recipes[random_recipe]['rodzaj'] == 'zupy') or (recipes[random_recipe]['rodzaj'] == 'dania-glowne')) and meal_counter == 3:
            daily_dinner.append(recipes[random_recipe]['nazwa'])
            meal_counter +=1
        elif (recipes[random_recipe]['rodzaj'] == 'sniadania-kolacje') and meal_counter > 3:
            daily_supper.append(recipes[random_recipe]['nazwa'])
            meal_counter +=1
        else:
            continue

        if kcal_daily + float(recipes[random_recipe]['kcal']) > kcal_limit + tollerance_kcal:
            break
        else:
            kcal_daily += float(recipes[random_recipe]['kcal'])
            protein_daily += float(recipes[random_recipe]['b'])
            carbs_daily += float(recipes[random_recipe]['ww'])
            fat_daily += float(recipes[random_recipe]['t'])

            # print('------------------------------------------------')
            # print(recipes[random_recipe]['nazwa'])
            # print(recipes[random_recipe]['rodzaj'])

    print('------------------------------------------------')
    print(f'kcal: {int(kcal_daily)} | b: {int(protein_daily)} | t: {int(fat_daily)} | ww: {int(carbs_daily)}')
    print(f'Procentowy rozkład makroskładników | b: {int(((protein_daily*4)/kcal_daily)*100)}% | t: {int(((fat_daily*9)/kcal_daily)*100)}% | ww: {int(((carbs_daily*4)/kcal_daily)*100)}%')

    print('------------------------------------------------')
    print(daily_breakfast)
    print(daily_dinner)
    print(daily_supper)


all_meals = load_json_from_file()

#print_all_recipes(all_meals)
#make_daily_menu(all_meals, 2300, 5)

#daily(all_meals, 2500, 3)

