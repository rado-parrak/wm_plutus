from baseObjects.page import Page
from scraperObjects.mappings import Mappings
import re

page_url = "https://www.sreality.cz/hledani/byty"

locators = {
    'checkBox': 'class|checkbox',
    'submitButton':'css|button.btn-full.btn-XL',
    'propertyListEntries':'class|title',
    'paging':'class|paging-item',
    'area':'class|area-cover',
    'numberOfResults':'',
    'propertyPageContent':'class|ng-scope',
    'attribute':'css|li.param.ng-scope',
    'attributeLabel':'css|label[class="param-label ng-binding"]',
    'attributeValue':'css|strong[class="param-value"] > span[class="ng-binding ng-scope"]'
}

class SelectionPage(Page):
    
    def open(self):
        self.driver.get(page_url)
        return self.wait_until_loaded()
        
    def wait_until_loaded(self):
        self.wait_for_available(locators['checkBox'])
        return self
        
    def tickOffCheckBoxes(self):
        elements = self.find_elements_by_locator(locators['checkBox'])
        counter = 0
        for element in elements:
            counter = counter + 1
            if counter < 22: # only first 21 checkboxes!
                if element.is_displayed():
                    element.click()
        return self
        
    def goToSelection(self):
        self.wait_for_available(locators['submitButton'])
        submitButton = self.find_element_by_locator(locators['submitButton'])
        submitButton.click()
        return self
    
    def setRegion(self, No):
        self.wait_for_available(locators['area'])
        regions = self.find_elements_by_locator(locators['area'])
        regions[No].click() # Prague is 10th region...

    def getNumberOfResults(self):
        self.wait_for_available(locators['submitButton'])
        submitButton = self.find_element_by_locator(locators['submitButton'])
        resultsNoString = submitButton.get_attribute('innerHTML')
        resultsNo = int(re.sub("[^0-9]", "", resultsNoString))
        return resultsNo
        
class PropertyList(Page):
            
        def getPropertyLinks(self):
            self.wait_for_available(locators['propertyListEntries'])
            elements = self.find_elements_by_locator(locators['propertyListEntries'])
            propertyLinks = []
            for element in elements:
                try:
                    propertyLinks.append(str(element.get_attribute("href")))
                except:
                    print("HREF not there...")
            return propertyLinks
        
        def NextPage(self):
            self.wait_for_available(locators['paging'])
            paginationSet = self.find_elements_by_locator(locators['paging'])
            paginationSet[11].click() # NEXT PAGE is the last button.
            
class PropertyPage(Page):
    
        def openPage(self, url):
            self.driver.get(url)
            return self.wait_until_loaded()
            
        def wait_until_loaded(self):
            self.wait_for_available(locators['propertyPageContent'])
            return self
            
        def getPropertyAttributes(self):
            self.wait_for_available(locators['attribute'])
            attributes = self.find_elements_by_locator(locators['attribute'])
            #print("Attributes count: " + str(len(attributes)) + ".")
            
            attribute_dictionary = {}
            attribute_dictionary['attributesNo'] = str(len(attributes));
            for attribute in attributes:
                try:
                    self.wait_for_available(locators['attributeLabel'])
                    attribute_name = attribute.find_element_by_locator(locators['attributeLabel'])
                    
                    self.wait_for_available(locators['attributeValue'])
                    attribute_value = attribute.find_element_by_locator(locators['attributeValue'])
                                       
                    attribute_dictionary = self.parseAttribute(attribute_dictionary
                                                                , attribute_name.text
                                                                , attribute_value.text)
                    #print(attribute_dictionary)
                except:
                    print("No attribute label or value found!!!")
                    
            return attribute_dictionary
        
        def parseAttribute(self, attribute_dictionary, attribute_name, attribute_value):
            
            attribute_name = re.sub('[^A-Za-z0-9]+', '', attribute_name)
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            mapper = Mappings()
            
            # -------- Celkova cena --------
            if(attribute_name == 'Celkovcena'):
                price = re.findall("\d+", attribute_value)
                price = ''.join(price)
                if(len(price) == 0 | price.isspace()):
                    attribute_dictionary["totalPrice"] = "NA"
                else:
                    attribute_dictionary["totalPrice"] = float(price)
                    
                del(price)
                    
            # -------- Cena --------
            if(attribute_name == 'Cena'):
                price = re.findall("\d+", attribute_value)
                price = ''.join(price)
                if(len(price) == 0 | price.isspace()):
                    attribute_dictionary["price"] = "NA"
                else:
                    attribute_dictionary["price"] = float(price)
                
                del(price)
            
            # -------- ID zakazky --------
            att = 'IDzakzky'
            if(attribute_name == att):
                attribute_dictionary['id'] = attribute_value
            
            # -------- Stavba: --------
            att = 'Stavba'
            if(attribute_name == att):
                attribute_dictionary['constructionType'] = mapper.mapConstructionType(attribute_value)
                

            # -------- Stav objeku: --------
            att = 'Stavobjektu'
            if(attribute_name == att):
                attribute_dictionary['constructionStatus'] = mapper.mapConstructionStatus(attribute_value)

            # -------- Stav objeku: --------
            att = 'Vlastnictv'
            if(attribute_name == att):
                attribute_dictionary['ownership'] = mapper.mapOwnership(attribute_value)

            # -------- UÃ…Â¾itnÃƒÂ¡ plocha: --------
            if(attribute_name == 'Uitnplocha'):
                area = re.findall("\d+", attribute_value)
                area = ''.join(area)
                if(len(area) == 0 | area.isspace()):
                    attribute_dictionary["livingArea"] = "NA"
                else:
                    attribute_dictionary["livingArea"] = float(area)
            
            # -------- Doprava: --------
            att = 'Doprava'
            if(attribute_name == att):
                attribute_dictionary['getByPublicTransport']    = mapper.mapGetByPublicTransport(attribute_value)
                attribute_dictionary['getByHighway']            = mapper.mapGetByHighway(attribute_value)
                attribute_dictionary['getByBus']                = mapper.mapGetByBus(attribute_value)
                attribute_dictionary['getByTrain']              = mapper.mapGetByTrain(attribute_value)
                attribute_dictionary['getByRoad']               = mapper.mapGetByRoad(attribute_value)

            # -------- EnergetickÃƒÂ¡ nÃƒÂ¡roÃ„ï¿½nost budovy: --------
            att = 'Energeticknronostbudovy'
            if(attribute_name == att):
                attribute_dictionary['energyEfficiency'] = mapper.mapEnergyEfficiency(attribute_value)

            # -------- Voda --------
            att = 'Voda'
            if(attribute_name == att):
                attribute_dictionary['water'] = attribute_value
                
            # -------- Balkon --------
            att = 'Balkn'
            if(attribute_name == att):
                attribute_dictionary['balcony'] = attribute_value
                
            # -------- Elektrina --------
            att = 'Elektina'
            if(attribute_name == att):
                attribute_dictionary['electricity'] = attribute_value
                
            # -------- Odpad --------
            att = 'Odpad'
            if(attribute_name == att):
                attribute_dictionary['sewer'] = attribute_value
                
            # -------- Topeni --------
            att = 'Topen'
            if(attribute_name == att):
                attribute_dictionary['heating'] = attribute_value
                
            # -------- Podlazi --------
            att = 'Podla'
            if(attribute_name == att):
                attribute_dictionary['floorNo'] = attribute_value
            
            return attribute_dictionary
    