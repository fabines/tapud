from cloudant.client import Cloudant
import os
import json
from cloudant.error import CloudantArgumentError
from cloudant.query import Query
from cloudant.result import QueryResult
import pandas as pd


def saveToHistory(db, List_input, list_View):
    doc_exist = 'order' in db
    if doc_exist:
        doc = db['order']
        doc.delete()
    newRow = {}
    newRow['_id'] = 'order'
    newRow['type'] = 'lastOrder'
    newRow['List_input'] = List_input
    newRow['list_view'] = list_View
    db.create_document(newRow)


def savePreferenceList(db, preferenceList):
    doc_exist = 'preference' in db
    if doc_exist:
        doc = db['preference']
        doc.delete()
    newRow = {}
    newRow['_id'] = 'preference'
    newRow['constraint'] = preferenceList
    db.create_document(newRow)


def getPreferenceList(db):
    doc_exist = 'preference' in db
    if doc_exist:
        doc = db['preference']
        return doc['constraint']
    else:
        return None


def getHistory(db):
    doc_exist = 'order' in db
    if doc_exist:
        doc = db['order']
        return doc
    else:
        return None


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
        fields=["שם חלקה מפורט", "איזור גידול", "_id","אבנים", "דונם לגידול שלחין",
                "אורגני", "מקור מים", "דוררת", "רגישות לקרה", "תיאור מיקום מדוייק", "גרב אבקי"],
    )
    return resp


def get4Years(db, currentYear):
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
                        currentYear-3,
                        currentYear-2,
                        currentYear-1
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

def getLastYear(db, currentYear):
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
                        currentYear-1
                    ]
                }
            },
            {
                "$nor": [
               {
                  "crop": "גזר"
               },
               {
                  "crop": "סלרי"
               },
               {
                  "crop": "פטרוזיליה"
               },
               {
                  "crop": "תפוא"
               }
            ]
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


def getAllPlots(db):
    query = Query(db)
    resp = query(
        selector={"type": {
                    "$eq": "plot"
                }}
    )
    return resp
