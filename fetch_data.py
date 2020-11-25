from extract import extract_data
import random
import pymysql
import re

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
    
