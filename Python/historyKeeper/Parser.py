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
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
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
                parser.updateHistory()
                parser.saveHistory()
                parser.moveToArchive()
                
    def elasticSearch_create_index(self,es_object, index_name='transactions'):
        created = False
        # index settings
        settings = {
            "mappings": {
                "_doc": {
                    "dynamic": "strict",
                    "properties": {
                        "accountNo": { "type": "text" },
                        "bookingDate" : { "type" : "date" },
                        "amount" : { "type" : "double" },
                        "currency" : { "type" : "text" },
                        "outstanding" : { "type" : "double" },
                        "targetAccountNo" : { "type" : "text" },
                        "targetBankCode" : { "type" : "text" },
                        "targetAccountName" : { "type" : "text" },
                        "constantSymbol" : { "type" : "text" },
                        "variableSymbol" : { "type" : "text" },
                        "specificSymbol" : { "type" : "text" },
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
        
    def elasticSearch_store_record(self, elastic_object, index_name, record, uid):
        try:
            outcome = elastic_object.index(index=index_name, doc_type='_doc', body=record, id = uid)
        except Exception as ex:
            print('Error in indexing data')
            print(str(ex))
     
    def updateElasticSearch(self):
        # fetch data from the intermediate store
        history = pd.read_pickle("../../03_data/transactions/_aggregated/transactional_history")
        
        # create index if not already there
        self.elasticSearch_create_index(self.es, index_name='transactions')
        
        # post the actual data
        for index, row in history.iterrows():
            self.elasticSearch_store_record(self.es, 'transactions', row.to_dict(), row['transactionId'])            
        print('ElasticSearch update done!')


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
        
        self.data['bookingDate'] = 

    def updateHistory(self):
        if(os.listdir("../../03_data/transactions/_aggregated").__contains__('transactional_history')):
            self.history = pd.read_pickle("../../03_data/transactions/_aggregated/transactional_history")
            # updating step:
            transactionId_inHistory = set(self.history['transactionId'])
            transactionId_inNew = set(self.data['transactionId'])
            newIds = transactionId_inNew - transactionId_inHistory
            non_duplicates = self.data[self.data['transactionId'].isin(newIds)]
            
            self.history = self.history.append(other = non_duplicates, sort=False).sort_values(by = 'bookingDate', ascending = False)
            
        else:
            self.history = self.data
    
    def saveHistory(self):
        self.history.to_pickle("../../03_data/transactions/_aggregated/transactional_history")
        
    def moveToArchive(self):
        os.rename(self.path + "/" + self.filename, self.path + "/_alreadyProcessed/" + self.filename)
        
        

            
        
        
        
        
        
        
        
        
        
        
        