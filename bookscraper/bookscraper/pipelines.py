# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        #strip al whitespace from string
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        #category & product type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        #price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        #availability --> extract number of book in stock
        availablity_string = adapter.get('availability')
        split_string_array = availablity_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availablity_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availablity_array[0])

        #Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        #stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == 'zero':
            adapter['stars'] = 0
        if stars_text_value == 'one':
            adapter['stars'] = 1
        if stars_text_value == 'two':
            adapter['stars'] = 2
        if stars_text_value == 'three':
            adapter['stars'] = 3
        if stars_text_value == 'four':
            adapter['stars'] = 4
        if stars_text_value == 'five':
            adapter['stars'] = 5
            
        return item

import mysql.connector
class SaveToMySqlPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'Rahelxv',
            database = 'books'
        )

        #create cursor, used to execute commands
        self.cur = self.conn.cursor()

        #create books table if non exists

        self.cur.execute(""" 
        CREATE TABLE IF NOT EXISTS books(
                         )
        """)