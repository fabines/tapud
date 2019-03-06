from cloudant.client import Cloudant
import os
import json
from cloudant.error import CloudantArgumentError
from cloudant.query import Query
from cloudant.result import QueryResult
import pandas as pd


def getSpecificPlot(id, db):
    query = Query(db)
    resp = query(
        selector={"$and": [
            {
                "_id": {
                    "$eq": id
                }
            },
            {
                "סוג חלקה": {
                    "$eq": "שלחין"
                }
            }
        ]},
        fields=["שם חלקה מפורט", "איזור גידול","_id" ,"אבנים",
                "דונם לגידול שלחין","אורגני","מקור מים","דוררת","רגישות לקרה","תיאור מיקום מדוייק","גרב אבקי"],
    )
    # selector={"$and": [
    #         {
    #             "_id": {
    #                 "$eq": id
    #             }
    #         },
    #         {
    #             "סוג חלקה": {
    #                 "$eq": "שלחין"
    #             }
    #         }
    #     ]}
    # docs = db.get_query_result(selector,fields=["שם חלקה מפורט", "אזור גידול","_id" ,"אבנים",
    #             "דונם לגידול שלחין","אורגני","מקור מים","דוררת","רגישות לקרה","גרב אבקי"])
    return resp


def get4Years(db):
    query = Query(db)
    resp = query(
        selector={"$and": [
            {
                "type": {
                    "$eq": "years"
                }
            },
            {
                "year": {
                    "$in": [
                        2016,
                        2017,
                        2018
                    ]
                }
            },
            {
                "crop": {
                    "$ne": "תפוא"
                }
            }
        ]},
        fields=["plot"],
    )
    return resp


def getSpecies(db):
    query = Query(db)
    resp = query(
        selector={"type": {
                    "$eq": "species"
                }},
        fields=["species","Variety","Skin_color","Mechanical_damage","Powdery_scab"]
    )
    return resp