'''
Created on Apr 11, 2019

@author: radov
'''
from scraper.baseObjects.page import Page
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from scraper.scraperObjects.mappings import Mappings
import datetime
from geopy.geocoders import Nominatim

class Crawler(Page):
    '''
    classdocs
    '''

    def __init__(self, driver):
        '''
        Constructor
        '''        
        self.driver = driver
        
    def goToPage(self, url):
        self.driver.get(url)
        
    def quit(self):
        self.driver.quit()
        
    def selectElements(self, locator, how, attribute_name, selector_set):
        elements = self.find_elements_by_locator(locator)
        for element in elements:
            if element.text in selector_set:
                if(how == "byText"):
                    if element.is_enabled():
                        element.click()
            if(how == "byAttribute"):    
                if element.get_attribute(attribute_name) in selector_set:
                    if element.is_enabled():
                        element.click()
                        
    def pushButton(self, locator):
        self.wait_for_available(locator)
        submitButton = self.find_element_by_locator(locator)
        submitButton.click()
        
    def getElementByLocator(self, locator):
        element = self.find_element_by_locator(locator) 
        return(element)
    
    def getElementsByLocator(self, locator):
        self.wait_for_available(locator)
        elements = self.find_elements_by_locator(locator) 
        return(elements)
        
    def getElementsByClassName(self, class_name):
        elements = self.find_elements_by_class_name(class_name) 
        return(elements)
    
    def goBack(self):
        self.driver.back()
        return(self)
    
    def waitUntilElementIsLoaded(self, param):
        timeout = 5
        
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, param))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            
    def parseAttribute(self, attribute_dictionary, attribute_name, attribute_value):
            
        attribute_name = re.sub('[^A-Za-z0-9]+', '', attribute_name)
        mapper = Mappings()

        # -------- Celkova cena --------
        if(attribute_name == 'Celkovcena'):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            price = re.findall("\d+", attribute_value)
            price = ''.join(price)
            if(len(price) == 0 | price.isspace()):
                attribute_dictionary["totalPrice"] = "NA"
            else:
                attribute_dictionary["totalPrice"] = float(price)
                
            del(price)
                
        # -------- Cena --------
        if(attribute_name == 'Cena'):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
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
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['constructionType'] = mapper.mapConstructionType(attribute_value)

        # -------- Stav objeku: --------
        att = 'Stavobjektu'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['constructionStatus'] = mapper.mapConstructionStatus(attribute_value)

        # -------- Stav objeku: --------
        att = 'Vlastnictv'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['ownership'] = mapper.mapOwnership(attribute_value)

        # -------- UÃ…Â¾itnÃƒÂ¡ plocha: --------
        if(attribute_name == 'Uitnplocha'):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            area = re.findall("\d+", attribute_value)
            area = ''.join(area)
            if(len(area) == 0 | area.isspace()):
                attribute_dictionary["livingArea"] = "NA"
            else:
                attribute_dictionary["livingArea"] = float(area)
        
        # -------- Doprava: --------
        att = 'Doprava'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['getByPublicTransport']    = mapper.mapGetByPublicTransport(attribute_value)
            attribute_dictionary['getByHighway']            = mapper.mapGetByHighway(attribute_value)
            attribute_dictionary['getByBus']                = mapper.mapGetByBus(attribute_value)
            attribute_dictionary['getByTrain']              = mapper.mapGetByTrain(attribute_value)
            attribute_dictionary['getByRoad']               = mapper.mapGetByRoad(attribute_value)

        # -------- EnergetickÃƒÂ¡ nÃƒÂ¡roÃ„ï¿½nost budovy: --------
        att = 'Energeticknronostbudovy'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['energyEfficiency'] = mapper.mapEnergyEfficiency(attribute_value)

        # -------- Voda --------
        att = 'Voda'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['water'] = attribute_value
            
        # -------- Balkon --------
        att = 'Balkn'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['balcony'] = attribute_value
            
        # -------- Elektrina --------
        att = 'Elektina'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['electricity'] = attribute_value
            
        # -------- Odpad --------
        att = 'Odpad'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['sewer'] = attribute_value
            
        # -------- Topeni --------
        att = 'Topen'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['heating'] = attribute_value
            
        # -------- Podlazi --------
        att = 'Podla'
        if(attribute_name == att):
            attribute_value = re.sub('[^A-Za-z0-9]+', '', attribute_value)
            attribute_dictionary['floorNo'] = attribute_value
            
        # -------- Aktualizace --------
        att = 'Aktualizace'
        if(attribute_name == att):
            if(re.sub('[^A-Za-z0-9]+', '', attribute_value) == "Dnes"):
                attribute_dictionary['updateDate'] = str(datetime.date.today().isoformat())
            else:
                attribute_dictionary['updateDate'] = datetime.datetime.strptime(attribute_value, '%d.%m.%Y').strftime('%Y-%m-%d')
        
        return attribute_dictionary
    
    
    def getGpsLocation(self, street, city):
        geo = Nominatim()
        try:
            coord = geo.geocode(street + ' ' + city, timeout = 10)
            latitude = coord.latitude
            longitude = coord.longitude
        except:
            latitude = None
            longitude = None
            print("Unable to fetch GPS location of street: " + street + " in the city of: " + city)
        
        return(latitude, longitude) 
        





        
        
        
        
