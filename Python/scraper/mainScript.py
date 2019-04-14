# import time
# import re
# from random import randint
from scraper.baseObjects.driver import WebDriver
# from scraperObjects.seznam import SelectionPage
# from scraperObjects.seznam import PropertyList
# from scraperObjects.seznam import PropertyPage

from scraper.crawler import Crawler

crawler = Crawler(driver = WebDriver())

# initial page
crawler.goToPage("https://www.sreality.cz/hledani/byty")
crawler.selectElements(locator = 'class|checkbox', how = "byText", selector_set = {"1+kk","1+1"}, attribute_name = None)
crawler.selectElements(locator = 'class|area-cover', how = "byAttribute", selector_set = {"area-cover praha","area-cover jihocesky"}, attribute_name = 'class')
crawler.pushButton(locator = 'css|button.btn-full.btn-XL')

# list of properties
aux = crawler.getElementsByLocator('css|.images.count3.clear')
propertiesOnPage = []
for propertyy in aux:
    try:
        print('Trying to scrape URL of property')
        propertiesOnPage.append(propertyy.get_attribute("href"))
    except Exception as e:
        print("URL could not be scraped")
        print("Exception: " + str(e))


for propertyUrl in propertiesOnPage:    
    # inside property page:
    crawler.goToPage(propertyUrl)
    crawler.waitUntilElementIsLoaded('content')
    
    # scrape property attributes
    atts = crawler.getElementsByLocator('css|li[class="param ng-scope"]')
    
    attribute_dictionary = {}
    attribute_dictionary['attributesNo'] = len(atts);
    for attribute in atts:
        try:
            crawler.wait_for_available('css|label[class="param-label ng-binding"]')
            attribute_name = attribute.find_element_by_locator('css|label[class="param-label ng-binding"]')
            
            crawler.wait_for_available('css|strong[class="param-value"] > span[class="ng-binding ng-scope"]')
            attribute_value = attribute.find_element_by_locator('css|strong[class="param-value"] > span[class="ng-binding ng-scope"]')
                               
            attribute_dictionary = crawler.parseAttribute(attribute_dictionary
                                                        , attribute_name.text
                                                        , attribute_value.text)
            #print(attribute_dictionary)
        except:
            print("No attribute label or value found!!!")
            
    # get LAT-LON from address
    city    = propertyUrl.split("/")[7].split("-")[0]
    street  = propertyUrl.split("/")[7].split("-")[-1]
    
    gps = crawler.getGpsLocation(street, city)
    attribute_dictionary['gps_latitude'] = gps[0]
    attribute_dictionary['gps_longtitude'] = gps[1]
    
    print("Latitude for " + street + ", " + city + " : [" + str(gps[0]) + ", " + str(gps[1]) + "].")

    print(attribute_dictionary)
    # go back
    crawler.goBack()
    
    

crawler.quit()

'''
# -- Set up driver:
chromeDriver = WebDriver()

# -- Open selection page and make selection --
selectionPage = SelectionPage(chromeDriver)
selectionPage.open()
selectionPage.selectFlatTypes()
selectionPage.selectRegions()
chromeDriver = selectionPage.goToSelection()

# -- run over properties --



propertiesCount = selectionPage.getNumberOfResults()


# -- Get the individual property links
numberOfPages = int((propertiesCount//20) + 1)
#numberOfPages = 1 
propertyLinkContainer = []
for i in range(numberOfPages):
    toWait = randint(1, 200)/100
    time.sleep(toWait)
    print('Page: '+ str(i) + ' | waited: ' + str(toWait))
    propertyList = PropertyList(driver)
    propertyLinkContainer.extend(propertyList.getPropertyLinks())
    try:
        propertyList.NextPage()
    except:
        break
        
    del propertyList

# -- Retreive the basic info from the links:
propertyBase = {}
counter = 0
for propertyLink in propertyLinkContainer:
    if propertyLink != 'None':
        counter = counter + 1
        try:
            info = {}
            aux = re.sub("https://www.sreality.cz/detail/prodej/byt/", "", propertyLink)
            apartmentType, apartmentArea, areaId = aux.split('/')
            info['apartmentType'] = apartmentType
            info['apartmentLocation'] = apartmentArea
    
            propertyBase[str(propertyLink)] = info
            del info
            del apartmentType
            del apartmentArea
        except:
            print("Property No. "+ str(counter)+" not saved to the propertyBase!")

for propertyLink in propertyBase:    
    counter += 1
    propertyPage = PropertyPage(driver)
    propertyPage.openPage(propertyLink)
    propertyBase[str(propertyLink)].update(propertyPage.getPropertyAttributes())

    # Insert a Person in the person table
    propertyy = propertyBase[str(propertyLink)]
    
    newPropertyToDb = Properties(pageAdress = str(propertyLink))
    for key in propertyy:
        exec('newPropertyToDb.'+ key + ' = "' + str(propertyy[key]) +'"')

    session.add(newPropertyToDb)
    print("Property " + str(counter)+ " added to DB!")
    if(counter % 25 == 0):
        session.commit()
        print("Results commited!")
        
session.commit()
session.close()
engine.dispose()

print("Over and out!")
'''    

