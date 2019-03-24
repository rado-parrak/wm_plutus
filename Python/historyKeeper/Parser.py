# -*- coding: utf-8 -*-

'''
Created on Mar 15, 2019

@author: Rado
'''
import pandas as pd 
import os
from elasticsearch import Elasticsearch
import datetime

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
                parser.categorise()
                parser.updateElasticSearch() 
                parser.moveToArchive()

class ParserCsob:
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename
    
    def parse(self):
        self.data = pd.read_csv(self.path + "/" + self.filename
                           , encoding = "ansi"
                           , header = 1
                           , delimiter = ";"
                           , index_col=False
                           , decimal = ',')

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
                            
    def moveToArchive(self):
        os.rename(self.path + "/" + self.filename, self.path + "/_alreadyProcessed/" + self.filename)

    def elasticSearch_store_record(self, elastic_object, index_name, record, uid):
        try:
            elastic_object.index(index=index_name, doc_type='_doc', body=record, id = uid)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))
     
    def updateElasticSearch(self):
        # initialize ES session
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        
        # create index if not already there
        self.elasticSearch_create_index(es, index_name='transactions')
        
        # post the actual data
        for index, row in self.data.iterrows():
            # TODO: Here should come a check if the record is not already in the DB
            self.elasticSearch_store_record(es, 'transactions', row.to_dict(), row['transactionId'])            
        print('ElasticSearch update done') 
        
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
                        "note" : { "type" : "text" }
                    }
                }
            }
        }
        try:
            if not es_object.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                es_object.indices.create(index=index_name, ignore=400, body=settings)
                print('Created Index')
                created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created   
        
        
    def categorise(self):
        self.data['transactionCategory'] = "unknown"
        
        for transaction in self.data.iterrows():
            if transaction['']
        
        
        
        
        
        