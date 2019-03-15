'''
Created on Mar 15, 2019

@author: Rado
'''
import pandas as pd 

class ParserCsob():
    
    def _init_(self):
        pass
    
    def parseRaw(self, path):
        self.data = pd.read_csv(path
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


    def updateHistory(self):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        