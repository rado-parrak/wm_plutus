'''
Created on Mar 28, 2019

@author: Rado
'''

class Categorizer():
    '''
    classdocs
    '''


    def __init__(self, rules, filename):
        '''
        Constructor
        '''
        self.rules = rules
        self.filename = filename
       
    def rulebasedCategorization(self, transactionData, categorizationTargetAttribute):
        if(categorizationTargetAttribute == "transactionPurpose"):            
            # run over the rules:            
            for e in self.rules:
                conditionHolder = ""
                for c in e['conditions']:
                    if(c['condition'] == " == "):
                        conditionHolder = conditionHolder + "(transactionData[" + c['conditionAttribute'] + "]" + c['condition']  + c['attributeValue'] + ")" + e['logicalOperator']
                    elif(c['condition'] == ".str.contains"):
                        conditionHolder = conditionHolder + "(transactionData[" + c['conditionAttribute'] + "]" + c['condition']  + "("+ c['attributeValue'] + "))" + e['logicalOperator']
                conditionHolder = conditionHolder[:-1]
                executionRule = "transactionData.loc[ " + conditionHolder + "," + e['categorizationTargetAttribute'] + "] = " + e['targetCategory']
                #print(executionRule)
                exec(executionRule)
                
            # save some categorization reports:
            self.filename = self.filename.replace(".csv","")
            transactionData['transactionPurpose'].value_counts().to_csv("valueCountsTransactionalPurpose" + self.filename + ".csv", header=False)
            transactionData[transactionData['transactionPurpose'] == 'unknown'].note.str.split(expand=True).stack().value_counts().head(50).to_csv("topUncategorizedWordsTransactionPurpose"+ self.filename +".csv", header=False)
        
        
        # transactionData.to_csv("test.csv", header=True)
        return(transactionData)