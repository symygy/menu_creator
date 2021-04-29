import requests
from bs4 import BeautifulSoup as bs
import random
import os
import re
import json

main_url = "https://michalwrzosek.pl/przepisy/kategoria/"
complete_recipe = {}


meal_types = ['dania-glowne', 'zupy', 'sniadania-kolacje']
#meal_types = ['zupy']

def create_request(meal_type, page):
    r_url = main_url + meal_type + f"/page/{page}?post_type=przepisy"
    print(r_url)
    return requests.get(r_url)

def create_soup(request):
    return bs(request.content, 'lxml')

def save_html_to_file(soup, file_name):
    with open(f'{file_name}.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def del_html_tags(txt):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', txt)

def recipes_macros(recipe):
    recipe_macros = recipe.select('.przepis-miniatura-opis .przepis-miniatura-makro-element > h5')
    return [macro.get_text() for macro in recipe_macros ]

def count_how_many_pages(soup):
    pages = soup.select('a.last')
    return pages[0].text

# def recipe_url(recipe):
#     urls_found = recipe.select('.przepis-miniatura > a')
#     print(urls_found)
#     #return [re.compile(r'//.+(.html)').search(str(url)).group().replace('//', 'http://') for url in urls_found]

def fetch_recipes_data(soup, meal_type):
    recipes = soup.find_all("div", {"class": "przepis-miniatura"})
    for index, recipe in enumerate(recipes):
        recipe_name = recipe.select('.przepis-miniatura-opis > h4')
        macro_values = recipes_macros(recipe)
        url = recipe.find('a', href=True)
        img = recipe.find('img', src=True)

        complete_recipe[recipe['data-id']] = {
            'nazwa' : del_html_tags(str(recipe_name[0])),
            'kcal' :  macro_values[0],
            'b' : macro_values[1],
            'ww' : macro_values[2],
            't' : macro_values[3],
            'rodzaj' : meal_type,
            'url' : url['href'],
            'img' : img['src']
        }
    return complete_recipe


def save_json_to_file(json_object):
    with open(f'json/recipes_database.json', 'w', encoding='utf-8') as f:
        f.write(json_object)

def create_dir_for_jsons():
    dir_path = f"{os.getcwd()}\json"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    return dir_path

print("Rozpoczynam pobieranie przepisów z adresów:")
create_dir_for_jsons()
for meal_type in meal_types:
    page_counter = 1
    response = create_request(meal_type, page_counter)
    soup_obj = create_soup(response)
    number_of_pages = count_how_many_pages(soup_obj)
    page_counter = 2

    while int(number_of_pages) >= page_counter:
        response = create_request(meal_type, page_counter)
        soup_obj = create_soup(response)
        found_recipes = fetch_recipes_data(soup_obj, meal_type)
        json_recipies = json.dumps(found_recipes, indent=6, ensure_ascii=False)
        page_counter += 1

save_json_to_file(json_recipies)

    # for k, v in found_recipes.items():
    #     print(f'Numer: {k}')
    #     print(f"{found_recipes[k]['id']} | kcal: {found_recipes[k]['kcal']} | b: {found_recipes[k]['b']} | ww: {found_recipes[k]['ww']} | t: {found_recipes[k]['t']}")
    #save_html_to_file(soup_obj, 'zupy')
