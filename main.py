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

    if choice=="1":

        urlpage = 'https://idcard.albany.edu/admin/patrongroups/patrongroups.php'
        print(urlpage)
        driver = selenium.webdriver.Firefox()

        driver.get(urlpage)


        # Get list of groups to scrape
        idcardgroups = []
        with open("idcardgroupnames.txt", 'r') as groupnames:
            for groupname in groupnames:
                pattern = r"^\d+ (.*)"
                match = re.search(pattern, groupname)
                idcardgroups.append(match.groups()[0])

        list1 = []

        for idcardgroup in idcardgroups:
            print("Position yourself at group '{0}' and then type '1' to continue".format(idcardgroup))

            if len(input("Continue?  ")) > 0:
                nameofgroup = idcardgroup
            else:
                break

            # print("Situate yourself on main page")
            # print("Select first group and enter group name")
            # nameofgroup = input("Group Name")

            # while nameofgroup != "quit":

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

                # driver.execute_script("wi=ndow.scrollTo(0,document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenofPage;")

            # nameofgroup = input("Enter next name of group")

            # Write out to JSON file at end
            f = open("output_tmp.json", "a")
            for item in list1:
                f.write(json.dumps(item, indent=4))
            f.close()

        with open("sample.json", "w") as outfile:
            json.dump(list1, outfile, skipkeys=False, ensure_ascii=True, check_circular=True,
                      allow_nan=True, cls=None, indent=None, separators=None)
