from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from googletrans import Translator
from sshtunnel import SSHTunnelForwarder
import pymysql
import re
from datetime import date
import time
import random
import sys






def extract_data(paragraph_text):

    distList = ['തിരുവനന്തപുരം', 'കൊല്ലം', 'എറണാകുളം', 'മലപ്പുറം', 'തൃശൂര്‍', 'ആലപ്പുഴ', 'കോട്ടയം', 'കോഴിക്കോട്','ഇടുക്കി', 'പാലക്കാട്', 'കണ്ണൂര്‍', 'കാസര്‍ഗോഡ്', 'പത്തനംതിട്ട', 'വയനാട്']
    
    #print(paragraph_text.split('.')[1])
    newCases = re.search( r'([0-9,]+)', paragraph_text.split('.')[0], re.M|re.I)
    #newCases = re.search( r'ഇന്ന് ([0-9]+) പേര്‍ക്കാണ് സംസ്ഥാനത്ത് കോവിഡ്-19 സ്ഥിരീകരിച്ചത്.', paragraph_text, re.M|re.I)
    distCases = re.search(r'((?s).*)രോഗ((?s).*)സ്ഥിരീകരിച്ചത്', paragraph_text.split('.', maxsplit = 1)[1].replace('.',','), re.M|re.I)
    #distCases = re.search( r'ഇന്ന് ([0-9]+) പേര്‍ക്കാണ് സംസ്ഥാനത്ത് കോവിഡ്-19 സ്ഥിരീകരിച്ചത്.((?s).*)ഇന്ന് രോഗ ബാധ സ്ഥിരീകരിച്ചത്.', paragraph_text, re.M|re.I)
    print(newCases.group())
    if distCases is not None:
        distCases = distCases.group(1)
    print(distCases)

    districtCount = [x for x in distCases.split(',')]
    #print(districtCount)

    dictionary = dict()
    translator = Translator() # initalize the Translator object
    d = date.today()
    dd = d.strftime("%d")
    mm = d.strftime("%m")
    y = d.strftime("%Y")

    #driver.find_element_by_tag_name('abbr')
    #dictionary['Date'] = str('"' + y +'-' + mm + '-' + dd + '"')
    #dictionary['Total'] = int(newCases.group())

    sameDist = []


    
    for dist in districtCount:
        for d in distList:
            if d in dist:
                if re.search(r'([0-9]+)', dist, re.M|re.I) is None:
                    sameDist.append(d)
                    continue
                if len(sameDist) > 0:
                    if re.search(r'([0-9]+)', dist, re.M|re.I) is None:
                        sameDist.append(d)
                        continue
                    else:
                        sameDist.append(d)
                        dictionary.update({el.text:re.search(r'([0-9]+)', dist, re.M|re.I).group() for el in translator.translate(sameDist)})
                        #print(sameDist)
                        #dictionary[(x.text) for x in translator.translate(sameDist)] = re.search(r'([0-9]+)', dist, re.M|re.I).group()
                        sameDist.clear()
                        continue
                    
                dictionary[translator.translate(d).text] = re.search(r'([0-9]+)', dist, re.M|re.I).group()
                #print(translator.translate(d).text +" => "+ re.search(r'([0-9]+)', dist, re.M|re.I).group()) 
            #print(d)
            #re.search(r'([0-9]+)', dist, re.M|re.I)
    total = 0
    
    for i in dictionary:
        total += int(dictionary[i])
        print (i, dictionary[i])
    #print(dist)
    
    
    if int(newCases.group(1).replace(',','')) == total:
        print("Count Check Success")
        dictionary['Date'] = str('"' + y +'-' + mm + '-' + dd + '"')
        dictionary['Total'] = int(newCases.group(1).replace(',',''))
        store_to_db(dictionary, True)
    else:
        print("Count Check Fail")
        
    #store_to_db(dictionary, True)        






def store_to_db(dictionary, use_tunnel):
    db_port = 3306
    if use_tunnel:
        #ssh to server
        server = SSHTunnelForwarder(
        ('192.168.0.110', 22),
        ssh_username='pi',
        ssh_password='gk',
        remote_bind_address=('127.0.0.1', 3306)
        )
    
        server.start()
        
        db_port = server.local_bind_port
        
    # Connect to the database
    db = pymysql.connect(
    host='127.0.0.1',
    port=db_port,
    user='admin',
    password='admin',
    db='covid_test'
    ,cursorclass=pymysql.cursors.DictCursor
    )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    fields = (str(list(dictionary.keys()))[1:-1])
    values = (str(list(dictionary.values()))[1:-1])

    # Insert a new record
    sql = 'INSERT INTO `DistrictCounts` (' + fields + ') VALUES (' + values + ')'
    # remove single Quotes
    sql = sql.replace('\'', '')
    #print(sql)
    cursor.execute(sql)
        
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    db.commit()

    db.close()

    db = pymysql.connect(
    host='127.0.0.1',
    port=db_port,
    user='admin',
    password='admin',
    db='covid19_kerala'
    ,cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()

    fields = (str(list(dictionary.keys()))[1:-1])
    values = (str(list(dictionary.values()))[1:-1])

    
    sql = 'INSERT INTO `district_count` (' + fields + ') VALUES (' + values + ')'
    
    sql = sql.replace('\'', '')
    
    cursor.execute(sql)

    db.commit()

    # disconnect from server
    db.close()

    sys.exit(0)






def selenium_extract(driver, url):
    
    words_list = [ "പേര്‍ക്കാണ്", "സംസ്ഥാനത്ത്", "കോവിഡ്-19", "സ്ഥിരീകരിച്ചത്"]
    #driver.get("http://mbasic.facebook.com")
    

    driver.get(url[0])
    #print(driver.page_source)
    articles = driver.find_elements_by_tag_name('article')
    #print(article)
    for a in articles:

        if any(word in a.text for word in words_list):
            
            link = a.find_element_by_link_text('More')
            link.click()

            p = driver.find_element_by_tag_name('p')
            print(p.text)

            post_time = driver.find_element_by_tag_name('abbr')

            print('Last Updated at ' + post_time.text)

            try :
                t = re.search( r'([0-9]+) (hr|hrs|min|mins)', post_time.text, re.M|re.I)
                if t is not None:
                    if ((t.group(2) == 'hr' or t.group(2) == 'hrs') and int(t.group(1)) < 6) or ((t.group(2) == 'min' or t.group(2) == 'mins') and int(t.group(1)) < 60 ):
                        extract_data(p.text)
                        
                    else :
                        rand_idx = random.choice(range(len(url)))
                        driver.get(url[rand_idx])
                        selenium_extract(driver, url)
                        #driver.quit() # cleanup code
                        
                #driver.quit()
                else :
                    rand_idx = random.choice(range(len(url)))
                    driver.get(url[rand_idx])
                    selenium_extract(driver, url)
                        

                        
            except pymysql.Error as err:
                print(err)
                driver.quit()
                
            finally:
                driver.quit() # cleanup code
            
            break
        
        #else:
    rand_idx = random.choice(range(len(url)))
    driver.get(url[rand_idx])
    selenium_extract(driver, url)
            

    driver.quit() # cleanup code
    
def login_to_fb(driver):
    driver.get("http://mbasic.facebook.com")
    username = driver.find_element_by_name("email")
    password = driver.find_element_by_name("pass")
    submit   = driver.find_element_by_name("login")
    username.send_keys("gauthamk48@yahoo.in")
    password.send_keys("@Gauthamk96")
    
    # Step 4) Click Login
    submit.click()
            
    
def intialize_driver(url):
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\gauth\Downloads\geckodriver-v0.27.0-win64\geckodriver.exe')
    login_to_fb(driver)
    driver.get(url)
    #driver.get("https://mbasic.facebook.com/CMOKerala/")
    return options, driver
    #driver.refresh()

    #selenium_extract(driver)


# start of script
data_url_list = ["https://mbasic.facebook.com/kkshailaja", "https://mbasic.facebook.com/CMOKerala/"]
#data_url = "https://mbasic.facebook.com/kkshailaja"
#data_url = "https://mbasic.facebook.com/CMOKerala/"
_,driver = intialize_driver(data_url_list[0])
selenium_extract(driver, data_url_list)
    

