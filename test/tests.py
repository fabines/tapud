import unittest
from model.solver import *
import sys

sys.path.append('../')


def fun(x):
    return x + 1


# class MyTest(unittest.TestCase):
#
#     def test(self):
#         self.assertEqual(fun(3), 4)


class TestAlgorithm(unittest.TestCase):

    # test 1: diseases and frost

    def test_diseases_frost(self):
        plots = [
            {
                "שם חלקה מפורט": "1",
                "איזור גידול": "בית קמה",
                "_id": "1",
                "דונם לגידול שלחין": 100,
                "אורגני": "רגיל",
                "מקור מים": "מאגר רהט",
                "דוררת": 1,
                "רגישות לקרה": None,
                "תיאור מיקום מדוייק": "1",
                "גרב אבקי": 30
            },
            {
                "שם חלקה מפורט": "2",
                "איזור גידול": "בית קמה",
                "_id": "2",
                "דונם לגידול שלחין": 100,
                "אורגני": "אורגני",
                "מקור מים": "מאגר רהט",
                "דוררת": 2,
                "רגישות לקרה": None,
                "תיאור מיקום מדוייק": "2",
                "גרב אבקי": 0
            },
            {
                "שם חלקה מפורט": "3",
                "איזור גידול": "משמר הנגב",
                "_id": "3",
                "דונם לגידול שלחין": 100,
                "אורגני": "רגיל",
                "מקור מים": "מאגר רהט",
                "דוררת": 0,
                "רגישות לקרה": "רגיש",
                "תיאור מיקום מדוייק": "3",
                "גרב אבקי": 0
            },
            {
                "שם חלקה מפורט": "4",
                "איזור גידול": "משמר הנגב",
                "_id": "4",
                "דונם לגידול שלחין": 100,
                "אורגני": "אורגני",
                "מקור מים": "מאגר רהט",
                "דוררת": 40,
                "רגישות לקרה": None,
                "תיאור מיקום מדוייק": "4",
                "גרב אבקי": 0
            }
        ]
        orders = [
            {
                # plot #2
                "id": 1,
                "organic": True,
                "type": "A",
                "date": "03-04-2019",
                "amount": 100,
                "stav": True,
                "sort": True,

            },
            {
                # plot #1
                "id": 2,
                "organic": False,
                "type": "B",
                "date": "03-02-2019",
                "amount": 100,
                "stav": False,
                "sort": True,

            },
            {
                # plot #3
                "id": 3,
                "organic": False,
                "type": "C",
                "date": "03-07-2019",
                "amount": 100,
                "stav": False,
                "sort": False,

            }
        ]

        variety = {"docs":
            [
                {
                    "Variety": "A",
                    "Skin_color": "red",
                    "Mechanical_damage": 2
                },
                {
                    "Variety": "B",
                    "Skin_color": "red",
                    "Mechanical_damage": 2
                },
                {
                    "Variety": "C",
                    "Skin_color": "red",
                    "Mechanical_damage": 2
                }
            ]
        }
        results = solve(plots, orders, variety, ["1", "2", "3", "4"])
        print("--------------------------------")
        print(results)
        for result in results['result']:
            if result['species']=='A':
                self.assertEqual(result['שם חלקה מפורט'], '2')
            elif result['species']=='B':
                self.assertEqual(result['שם חלקה מפורט'], '1')
            else:
                self.assertEqual(result['שם חלקה מפורט'], '3')
