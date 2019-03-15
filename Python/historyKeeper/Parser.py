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

        self.data = self.data.rename(columns={"��slo ��tu": "accountNo"
                                    , "datum za��tov�n�": "bookingDate"
                                    , "��stka" : "amount"
                                    , "m�na" : "currency"
                                    , "z�statek" : "outstanding"
                                    , "��slo ��tu proti��tu" : "targetAccountNo"
                                    , "k�d banky proti��tu" : "targetBankCode"
                                    , "n�zev ��tu proti��tu" : "targetAccountName"
                                    , "konstantn� symbol" : "constantSymbol"
                                    , "variabiln� symbol" : "variableSymbol"
                                    , "specifick� symbol" : "specificSymbol"
                                    , "ozna�en� operace" : "transactionName"
                                    , "ID transakce" : "transactionId"
                                    , "pozn�mka" : "note"})


    def updateHistory(self):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        