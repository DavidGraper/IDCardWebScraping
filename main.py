import json
import re

import selenium
from selenium.webdriver.common.by import By

def processnullabledate(inputstring):

    if inputstring == "":
        return "NULL"
    else:
        yearstring = inputstring[6:10]
        datestring = inputstring[3:5]
        monthstring = inputstring[0:2]
        return "'{0}-{1}-{2}'".format(yearstring, monthstring, datestring)


if __name__ == '__main__':

    # Go to UAlbany IDCards page
    urlpage = 'https://idcard.albany.edu/admin/patrongroups/patrongroups.php'
    driver = selenium.webdriver.Firefox()
    driver.get(urlpage)

    # Get predefined list of ID card groups to scrape
    idcardgroups = []
    with open("idcardgroupnames.txt", 'r') as groupnames:
        for groupname in groupnames:
            pattern = r"^\d+ (.*)"
            match = re.search(pattern, groupname)
            idcardgroups.append(match.groups()[0])

    # Initialize list to hold dictionary entries for each ID card record
    list1 = []

    # Loop through ID card groups
    for idcardgroup in idcardgroups:

        # This version requires a human to manually position the browser to a specific
        # group and then agree to "continue" to scrape that page for that group
        print("Position yourself at group '{0}' and then type '1' to continue".format(idcardgroup))

        if len(input("Continue?  ")) > 0:
            nameofgroup = idcardgroup
        else:
            break

        ualbanyids = driver.find_elements(By.CLASS_NAME, 'td-PIK')
        names = driver.find_elements(By.CLASS_NAME, 'td-NAME')
        startdates = driver.find_elements(By.CLASS_NAME, 'td-GROUPEFFECTIVE')
        enddates = driver.find_elements(By.CLASS_NAME, 'td-GROUPEXPIRE')
        comments = driver.find_elements(By.CLASS_NAME, 'td-THECOMMENT')
        createdate = driver.find_elements(By.CLASS_NAME, 'td-CREATEDATE')
        operatorname = driver.find_elements(By.CLASS_NAME, 'td-OPERATORNAME')
        membertype = driver.find_elements(By.CLASS_NAME, "td-MEMBERTYPE")

        # - elements = driver.find_elements(By.CLASS_NAME, 'author')

        counter = 0
        for ualbanyid in ualbanyids:
            tempdict = {"nameofgroup": nameofgroup}
            tempdict["ualbanyempid"] = ualbanyid.text
            tempdict["name"] = names[counter].text
            tempdict["startdate"] = startdates[counter].text
            tempdict["enddate"] = enddates[counter].text
            tempdict["comment"] = comments[counter].text
            tempdict["createdate"] = createdate[counter].text
            tempdict["operatorname"] = operatorname[counter].text
            tempdict["membertype"] = membertype[counter].text

            list1.append(tempdict)
            counter += 1

    # Once all entries have been cached, write it all out as a JSON file
    with open("ualbanyidcards.json", "w") as outfile:
        json.dump(list1, outfile, skipkeys=False, ensure_ascii=True, check_circular=True,
                  allow_nan=True, cls=None, indent=None, separators=None)
