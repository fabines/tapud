from cloudant.client import Cloudant
import os
import json
from getFromDB import *
from cloudant.error import CloudantArgumentError
from cloudant.query import Query
from cloudant.result import QueryResult
import pandas as pd



class first_try:
    def __init__(self):
        db=None

    def connection_to_database(self):
        if os.path.isfile('../resources/vcap-local.txt'):
            with open('../resources/vcap-local.txt') as f:
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
        self.db = my_database
        my_document = my_database.client['batya_db']
       # crops4years= self.get4Years(self, 2018, self.db)
        return my_database

    def getPlots(self,db,orders):
        plots= get4Years(db)
        newListPlots=[]
        for plot in plots['docs']:
            newListPlots.append(plot['plot'])
        countPlots=dict((x, newListPlots.count(x)) for x in set(newListPlots))
        potPlots=[]
        for key,value in countPlots.items():
            if(value==3):
                potPlots.append(key)
        newListPlots = []
        for plot in potPlots:
            newListPlots.append(getSpecificPlot(plot,db))
        print(newListPlots)
        #newPlots=list({v['plot']: v for v in plots['docs']}.values())
        result=[]
        # for plot in potPlots:
        #     getShalhin=getSpecificPlot(plot,db)
        #     if getShalhin['docs']:
        #         amount=getShalhin['docs'][0]
        #         if requiredArea>amount.get('דונם לגידול שלחין'):
        #             result.append(amount)
        #             requiredArea -= amount.get('דונם לגידול שלחין')
        #         else:
        #             amount['דונם לגידול שלחין']=requiredArea
        #             result.append(amount)
        #             return result






