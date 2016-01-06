# https://dzone.com/articles/how-download-file-python

import urllib2

root_url = 'http://www.semanda.com/pdf/'
urls = ['flashcards_animals.pdf', 'flashcards_animals_pinyin.pdf', 'flashcards_body.pdf', 'flashcards_body_pinyin.pdf', 'flashcards_cities.pdf', 'flashcards_cities_pinyin.pdf', 'flashcards_clothes.pdf', 'flashcards_clothes_pinyin.pdf', 'flashcards_colors.pdf', 'flashcards_colors_pinyin.pdf', 'flashcards_countries.pdf', 'flashcards_countries_pinyin.pdf', 'flashcards_directions.pdf', 'flashcards_directions_pinyin.pdf', 'flashcards_drinks.pdf', 'flashcards_drinks_pinyin.pdf', 'flashcards_electronics.pdf', 'flashcards_electronics_pinyin.pdf', 'flashcards_food.pdf',
        'flashcards_food_pinyin.pdf', 'flashcards_fruits.pdf', 'flashcards_fruits_pinyin.pdf', 'flashcards_furniture.pdf', 'flashcards_furniture_pinyin.pdf', 'flashcards_nature.pdf', 'flashcards_nature_pinyin.pdf', 'flashcards_numbers.pdf', 'flashcards_numbers_pinyin.pdf', 'flashcards_restaurant.pdf', 'flashcards_restaurant_pinyin.pdf', 'flashcards_toys.pdf', 'flashcards_toys_pinyin.pdf', 'flashcards_weather.pdf', 'flashcards_weather_pinyin.pdf', 'flashcards_vegetables.pdf', 'flashcards_vegetables_pinyin.pdf', 'flashcards_vehicles.pdf', 'flashcards_vehicles_pinyin.pdf']

for file_name_url in urls:
    file_name = file_name_url
    f = urllib2.urlopen(root_url + file_name_url)
    data = f.read()
    with open(file_name, "wb") as code:
        code.write(data)