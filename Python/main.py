'''
Created on Jul 26, 2018

@author: Rado
'''
from historyKeeper.Parser import Parser

parser = Parser(list(["CSOB"]))
parser.parse()
parser.updateElasticSearch()


# record = {
#    "accountNo": "123",
#     "bookingDate" : datetime.datetime(2009, 10, 5, 18, 0),
#     "amount" : 123.4,
#     "currency" : "CZK",
#     "outstanding" : 12336.5,
#     "targetAccountNo" : "AAB/23",
#     "targetBankCode" : "0300",
#     "targetAccountName" : "Taki",
#     "constantSymbol" : "",
#     "variableSymbol" : "",
#     "specificSymbol" : "",
#     "transactionName" : "",
#     "transactionId" : "1",
#     "note" : "Hi there!"
# }



print("End")


#===============================================================================
# from calculator import Calculator
# from initialize import Initialize
# # --- INITIALIZE ---
# rredis = Initialize();
# 
# # --- DO CALCULATIONS ---
# calc = Calculator(rredis, 'root')
# calc.run()
# 
# # i) calculate outstandings on all instruments:
# #calc.projectOutstandings()
# 
# print('Calculation done!')
#===============================================================================
    


