from intialize import intialize_driver
from fetch_data import selenium_extract

def main():
    
    # start of script
    data_url_list = ["https://mbasic.facebook.com/kkshailaja", "https://mbasic.facebook.com/CMOKerala/"]

    _,driver = intialize_driver(data_url_list[0])
    selenium_extract(driver, data_url_list)

if __name__ == "__main__" :
    main()
