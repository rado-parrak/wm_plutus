'''
Created on Jul 26, 2018

@author: Rado
'''
from historyKeeper.Parser import Parser

parser = Parser(list(["CSOB"]))
parser.parse()

print("historyKeeper done!")


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
    


