from cloudant.client import Cloudant
import os
import json
import pandas as pd
from model.main import *

f = first_try()
db = f.connection_to_database()
plots=f.getPlots(db,400)
print(plots)
#result=f.get4Years(1,db)
#data = pd.read_csv('./resources/new_table.csv', encoding='windows-1255')

# data_json = json.loads(data.to_json(orient='records'))
# for row in data_json:
#     row['דונם לגידול שלחין']=int(row['דונם לגידול שלחין'])
#     #print(row)
#     db.create_document(row)


# data = pd.read_csv('./resources/years.csv', encoding='windows-1255')
#
# data_json = json.loads(data.to_json(orient='records'))
#
# for row in data_json:
#     for key, value in row.items():
#         if key=='plot' or value is None:
#             continue
#         newRow = {}
#         newRow['plot']=row['plot']
#         newRow['year']=int(key)
#         newRow['crop']=value
#         newRow['type']='years'
#         #print (newRow)
#         db.create_document(newRow)
