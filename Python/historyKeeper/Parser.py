# -*- coding: utf-8 -*-

'''
Created on Mar 15, 2019

@author: Rado
'''
import pandas as pd 
import numpy as np
import os
from elasticsearch import Elasticsearch
import datetime
from categorization import categorizer
import json

class Parser:
    def __init__(self, parserFlavourList):
        self.parsefFlavourList = parserFlavourList
    
    def parse(self):
        if("CSOB" in self.parsefFlavourList):
            path = "../../03_data/transactions/CSOB"
            # get all CSOB-files in the directory:
            files = os.listdir(path)
            files = [k for k in files if 'pohyby-na' in k]
            for file in files:
                parser = ParserCsob(path = path, filename = file)
                parser.parse()
                # TODO: Categorisation should be moved to a dedicated class
                parser.categorise("./categorization/categorizationRulesDefinitions.json", filename = file)
                parser.updateElasticSearch(file) 
                # parser.moveToArchive()

class ParserCsob:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
    
    def parse(self):
        schema={"èíslo úètu": np.str, 
                "datum zaúètování": np.str,
                "èástka": np.float,
                "mìna" : np.str,
                "zùstatek" : np.float,
                "èíslo úètu protiúètu" : np.str,
                "kód banky protiúètu" : np.str,
                "název úètu protiúètu" : np.str,
                "konstantní symbol" : np.str,
                "variabilní symbol" : np.str,
                "specifický symbol" : np.str,
                "oznaèení operace" : np.str,
                "ID transakce" : np.str,
                "poznámka" : np.str}
        
        
        self.data = pd.read_csv(self.path + "/" + self.filename
                           , encoding = "ansi"
                           , header = 1
                           , delimiter = ";"
                           , index_col=False
                           , decimal = ','
                           , dtype = schema)

        self.data = self.data.rename(columns={"èíslo úètu": "accountNo"
                                    , "datum zaúètování": "bookingDate"
                                    , "èástka" : "amount"
                                    , "mìna" : "currency"
                                    , "zùstatek" : "outstanding"
                                    , "èíslo úètu protiúètu" : "targetAccountNo"
                                    , "kód banky protiúètu" : "targetBankCode"
                                    , "název úètu protiúètu" : "targetAccountName"
                                    , "konstantní symbol" : "constantSymbol"
                                    , "variabilní symbol" : "variableSymbol"
                                    , "specifický symbol" : "specificSymbol"
                                    , "oznaèení operace" : "transactionName"
                                    , "ID transakce" : "transactionId"
                                    , "poznámka" : "note"})
        
        # Data cleaning:
        # - turn date strings into datetimes:
        self.data['bookingDate'] =  pd.to_datetime(self.data['bookingDate'], format='%d.%m.%Y')
        
        # - adjust txnID
        self.data['transactionId'] = "CSOB_" + self.data['transactionId'].astype(str) 
        
        # - get rid of NaNs:
        if self.data.isnull().values.any():
            for col in self.data:
                if self.data[col].isnull().values.any():
                    if col in {"accountNo", "currency", "targetAccountNo", "targetBankCode", "targetAccountName", "constantSymbol", "variableSymbol", "specificSymbol", "transactionName", "transactionId", "note"}:
                        self.data[col].fillna('missing', inplace = True)
                    if col in {"amount", "outstanding"}:
                        self.data[col].fillna(0.0, inplace = True)
                    if col in {"bookingDate"}:
                        self.data[col].fillna(datetime.datetime(1970, 1, 1, 0, 0), inplace = True)
                        
        # add categorization place holders for new transactions:
        self.data['transactionType'] = "unknown"
        self.data['transactionPurpose'] = "unknown"
        #self.data['transactionCategorizationDate'] = None
        
        # text field cleaning
        self.data['transactionName'] = self.data['transactionName'].str.replace('[^A-Za-z\s]+','').str.lower()        
        self.data['note'] = self.data['note'].str.replace('[^A-Za-z\s]+','').str.lower()
        self.data['note'] = self.data['note'].str.replace('\s+',' ')
        self.data['note'] = self.data['note'].str.replace(' ','_')
        self.data['note'] = self.data['note'].fillna('***MISSING***')
        
        # internal / external transactions
        self.data['isInternal'] = False
        self.data.loc[self.data['targetAccountNo'] == "217207635", ['isInternal']] = True
        self.data.loc[self.data['targetAccountNo'] == "261846266", ['isInternal']] = True
        self.data.loc[self.data['targetAccountNo'] == "273810949", ['isInternal']] = True
        self.data.loc[ (self.data['targetAccountNo'] == "2701115563") & (self.data['targetBankCode'] == "2010"), ['isInternal']] = True
                            
    def moveToArchive(self):
        os.rename(self.path + "/" + self.filename, self.path + "/_alreadyProcessed/" + self.filename)

    def elasticSearch_store_record(self, elastic_object, index_name, record, uid):
        try:
            elastic_object.index(index=index_name, doc_type='_doc', body=record, id = uid)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))
     
    def updateElasticSearch(self, filename):
        # initialize ES session
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        # create index if not already there
        self.elasticSearch_create_index(es, index_name='transactions')
        
        # post the actual data
        for index, row in self.data.iterrows():
            if(not es.exists(index="transactions", doc_type='_doc', id=row['transactionId'])):
                self.elasticSearch_store_record(es, 'transactions', row.to_dict(), row['transactionId'])            
        print('ElasticSearch | updated for file: '+ filename) 
        
    def elasticSearch_create_index(self,es_object, index_name='transactions'):
        created = False
        # index settings
        settings = {
            "mappings": {
                "_doc": {
                    "dynamic": "strict",
                    "properties": {
                        "accountNo": { "type": "keyword" },
                        "bookingDate" : {
                            "type":   "date",
                            "format": "date_hour_minute_second"
                            },
                        "amount" : { "type" : "double" },
                        "currency" : { "type" : "keyword" },
                        "outstanding" : { "type" : "double" },
                        "targetAccountNo" : { "type" : "text" },
                        "targetBankCode" : { "type" : "keyword" },
                        "targetAccountName" : { "type" : "text" },
                        "constantSymbol" : { "type" : "keyword" },
                        "variableSymbol" : { "type" : "keyword" },
                        "specificSymbol" : { "type" : "keyword" },
                        "transactionName" : { "type" : "text" },
                        "transactionId" : { "type" : "text" },
                        "note" : { "type" : "text" },
                        "transactionType" : { "type" : "keyword" },
                        "transactionPurpose" : { "type" : "keyword" },
                        "isInternal" : { "type" : "keyword" },                                                
                    }
                }
            }
        }
        try:
            if not es_object.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                es_object.indices.create(index=index_name, ignore=400, body=settings)
                print('ElasticSearch | created index: '+ index_name)
                created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created   
        
        
    def categorise(self, rulesPath, filename):
        # i) load in rules
        with open(rulesPath, 'r') as f:
            rules = json.load(f)
        # ii) initialize categorization
        catt = categorizer.Categorizer(rules, filename)
        
        # iii) rule-based categorisation        
        self.data = catt.rulebasedCategorization(self.data, categorizationTargetAttribute = "transactionType")
        self.data = catt.rulebasedCategorization(self.data, categorizationTargetAttribute = "transactionPurpose")

        # ii) scoring model based categorisation:
        # TODO: Not implemented yet...
        
        
        
        
        
        