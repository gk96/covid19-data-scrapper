import re
from datetime import date
import time
from googletrans import Translator
from store import store_to_db

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
                if re.search(r'([0-9]+)', dist, re.M|re.I) is not None:    
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
