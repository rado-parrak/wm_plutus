import time
import re
from random import randint
from baseObjects.driver import WebDriver
from scraperObjects.seznam import SelectionPage
from scraperObjects.seznam import PropertyList
from scraperObjects.seznam import PropertyPage

# -- Set up driver:
chromeDriver = WebDriver()

# -- Open selection page:
selectionPage = SelectionPage(chromeDriver)
selectionPage.open()
selectionPage.selectFlatTypes()
selectionPage.selectRegions()

'''
propertiesCount = selectionPage.getNumberOfResults()
selectionPage.goToSelection()

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

