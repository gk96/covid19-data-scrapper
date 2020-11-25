from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options

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
    #options = Options()
    #options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    #driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\gauth\Downloads\geckodriver-v0.27.0-win64\geckodriver.exe')
    #login_to_fb(driver)
    driver.get(url)
    
    return options, driver
   

    
