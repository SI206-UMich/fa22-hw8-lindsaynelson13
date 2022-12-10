import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute("SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants JOIN buildings JOIN categories ON buildings.id = restaurants.building_id AND categories.id = restaurants.category_id")

    restaurant_dict = []

    for restaurant in cur.fetchall():
        d = {}
        d['name'] = restaurant[0]
        d['category'] = restaurant[1]
        d['building'] = restaurant[2]
        d['rating'] = restaurant[3]
        restaurant_dict.append(d)

    return restaurant_dict

    pass

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    cur.execute("SELECT categories.category, COUNT(restaurants.category_id) FROM restaurants JOIN categories ON categories.id = restaurants.category_id GROUP BY categories.category")

    category_dict = {}

    for category in cur.fetchall():
        category_dict[category[0]] = category[1]

    sorted_category_dict = sorted(category_dict.items(), key = lambda x:x[1])
    sorted_dict = dict(sorted_category_dict)

    plt.barh(list(sorted_dict.keys()), list(sorted_dict.values()))
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Restaurant Categories')
    plt.title('Kinds of Restaurants on South U')
    plt.tight_layout()
    plt.show()


    return category_dict


    pass


#Try calling your functions here
def main():
    db_filename = "South_U_Restaurants.db"
    get_restaurant_data(db_filename)
    barchart_restaurant_categories(db_filename)
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
