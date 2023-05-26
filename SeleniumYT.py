'''

Selenium Youtube Transcriber

'''

import sys
import time
from sys import platform
import os

if "selenium" in str(sys.modules.keys()):
    import selenium
    print(selenium.version)
else:
    pass
    #print(sys.modules.keys())
    #print("Selium package not found! Aborting")


from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By

MAX_TRIES = 1000

def startService():
    '''
    Locate the service file and start it
    '''
    print("Detecting OS")
    if platform == "linux" or platform == "linux2":
        driver_name = "/usr/bin/chromedriver"
    elif platform == "darwin":
        driver_name = "/Applications/chromedriver/chromedriver"
    elif platform == "win32":
        driver_name = "C:\Program Files\Google\chromedriver\chromedriver.exe"

    if not os.path.exists(driver_name):
        print("Failed to find chrome driver on system type: " + platform)
        print("Please check install: " + driver_name)
        return None

    print("Atempting service start on: " + platform)
    try:
        webdriver_service = service.Service(driver_name)
        webdriver_service.start()
    except:
        print("Failed to start webdriver service: " + webdriver_service)
        return None

    print("Sucessfully started service")
    return webdriver_service


def startDriver(webdriver_service=None):
    '''
    Start chrome Driver from the service with options
    '''
    print("Setting driver options...")
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', True)
    options.add_argument("--window-size=2560,1440")
    #options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox") 
    #options.add_argument("--disable-setuid-sandbox") 
    #options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-dev-shm-using") 
    #options.add_argument("--disable-extensions") 
    options.add_argument("--disable-gpu") 
    #options.add_argument("start-maximized") 
    #options.add_argument("disable-infobars")
    
    print("Atempting to start driver from webservice")
    try:
        if webdriver_service == None:
            print("DEEEBUGGGG")
            if platform == "win32":
                driver = webdriver.Chrome('chromedriver.exe', options=options)
            else:
                driver = webdriver.Chrome('chromedriver', options=options)
        else:
            driver = webdriver.Remote(webdriver_service.service_url, options=options)
    except Exception as e:
        print(" Failed to start driver: ")
        print(e)
        return None
    print(" Driver Started Sucessfully")
    return driver


def getTranscription(service, url):
    '''
    '''
    i = 0

    if (service == None) or (url == ""):
        return

    print("Atempting Load")
    for _ in range(MAX_TRIES):
        try:
            # Load url
            driver = startDriver(service)
            driver.get(url)
            time.sleep(10)

            print(" Loaded Page, finding app..")
            
            # Load app by tag
            app = driver.find_element(By.TAG_NAME, 'ytd-app')
            time.sleep(5)

            print(" Opening Actions Menu")

            # Locate and click actions button
            content = app.find_element(By.ID, 'content')
            pg_mgr = driver.find_element(By.ID, 'page-manager')
            col = pg_mgr.find_element(By.ID, 'columns')
            below = col.find_element(By.ID, 'below')
            actions = below.find_element(By.ID, 'actions')
            button = actions.find_element(By.ID, 'button-shape')
            button.click()
            print("  Action menu clicked")
            break
        except:
            print("Load Failed... " + str(i))
            if driver != None:
                driver.close()
            time.sleep(1)
            pass
    time.sleep(5)

    print(" Locating popup menu")
    # Locate and click transcript button in actions dropdown
    popup = driver.find_element(By.TAG_NAME, 'ytd-popup-container')
    dropdowns = popup.find_elements(By.TAG_NAME, 'tp-yt-iron-dropdown')

    print("  Selecting Show Transcript action")
    for dropdown in dropdowns:
        if (dropdown.is_displayed()):
            items = dropdown.find_elements(By.TAG_NAME, 'ytd-menu-service-item-renderer')
            for item in items:
                if "transcript" in item.text:
                    item.click()
                    print("  Transcript enabled")
                    break
            break
    time.sleep(5)

    print(" Locating Transcript")
    # Download Transcript
    for _ in range(MAX_TRIES):
        try:
            sec = col.find_element(By.ID, 'secondary')
            panels = sec.find_element(By.ID, 'panels')
            sections = panels.find_elements(By.TAG_NAME, 'ytd-engagement-panel-section-list-renderer')

            for section in sections:
                if "EXPANDED" in section.get_attribute('visibility'):
                    print("  Transcript found and downloaded")
                    transcript = section.text
                    break
            break
        except:
            time.sleep(1)
            pass

    print("Close webdriver")
    # close driver
    driver.close()

    print("Save Transcript")
    # Write transcript to file
    if "watch?v=" in url:
        filename = url.lstrip("https://www.youtube.com/watch?v=") + "_syt.txt"
    else:
        filename = 'transcript_syt.txt'
        
    outfile = open(filename, 'w')
    outfile.write(transcript)
    outfile.close()

    return transcript


if __name__ == "__main__":
    # Example transcript
    url = "https://www.youtube.com/watch?v=FymR0rKdLZo"

    # Start Service
    service = startService()
    if service != None:
        # Open the Chrome driver
        getTranscription(service, url)



    
