class Mappings():
    '''
    classdocs
    '''
    
    def mapConstructionType(self, constructionType):
        
        output = { 'Cihlov': 'bricks'
                  ,'Panelov': 'concrete'
                  , 'Smen' : 'mixed'
                  , 'Skeletov' : 'skelet'
                  }.get(constructionType, constructionType)
                
        return output

    def mapConstructionStatus(self, constructionStatus):
        
        output = { 'Velmidobr': 'Very good'
                  , 'Dobr' : 'Good'
                  , 'Porekonstrukci' : 'After reconstruction'
                  , 'Novostavba' : 'Brand new'
                  , 'Vevstavb' : "Under construction"
                  , 'Pedrekonstrukc' : 'Before reconstruction'
                  }.get(constructionStatus, constructionStatus)
                
        return output
    
    def mapOwnership(self, ownership):
        
        output = { 'Osobn' : 'private'
                  ,'Drustevn' : 'cooperative aparment' 
                    
                  }.get(ownership, ownership)
                
        return output
    
    def mapEnergyEfficiency(self, energyEfficiency):                
        return energyEfficiency[3]
    
    def mapGetByPublicTransport(self, input):
        indicator = '0'
        if("MHD" in input):
            indicator = '1'
        return indicator
    
    def mapGetByHighway(self, input):
        indicator = '0'
        if("Dlnice" in input):
            indicator = '1'
        return indicator
    
    def mapGetByBus(self, input):
        indicator = '0'
        if("Autobus" in input):
            indicator = '1'
        return indicator
    
    def mapGetByTrain(self, input):
        indicator = '0'
        if("Vlak" in input):
            indicator = '1'
        return indicator
    
    def mapGetByRoad(self, input):
        indicator = '0'
        if("Silnice" in input):
            indicator = '1'
        return indicator