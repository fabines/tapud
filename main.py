from cloudant.client import Cloudant
import os
import json
import pandas as pd
from model.main import *

# f = first_try()
# db = f.connection_to_database()
# plots=f.getPlots(db,400)
# print(plots)
#result=f.get4Years(1,db)
if os.path.isfile('./resources/vcap-local.txt'):
    with open('./resources/vcap-local.txt') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True, auto_renew=True)

session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))

my_database = client['batya_db']
db = my_database
my_document = my_database.client['batya_db']
# crops4years= self.get4Years(self, 2018, self.db)

data = pd.read_csv('./resources/species.csv', encoding='windows-1255')

data_json = json.loads(data.to_json(orient='records'))
for row in data_json:
    if row['Powdery_scab'] is not None:
        row['Powdery_scab']=int(row['Powdery_scab'])
    if row['Mechanical_damage'] is not None:
        row['Mechanical_damage'] = int(row['Mechanical_damage'])
    print(row)
    db.create_document(row)


# data  = pd.read_csv('./resources/years.csv', encoding='windows-1255')
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
