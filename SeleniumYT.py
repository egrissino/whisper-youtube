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

MAX_TRIES = 20

DEBUG = True

def printDebug(msg):
    if DEBUG:
        print(msg)


def startService():
    '''
    Locate the service file and start it
    '''
    printDebug("Detecting OS")
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

    printDebug("Atempting service start on: " + platform)
    try:
        webdriver_service = service.Service(driver_name)
        webdriver_service.start()
    except:
        printDebug("Failed to start webdriver service: " + webdriver_service)
        return None

    printDebug("Sucessfully started service")
    return webdriver_service


def startDriver(webdriver_service=None):
    '''
    Start chrome Driver from the service with options
    '''
    printDebug("Setting driver options...")
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
    
    printDebug("Atempting to start driver from webservice")
    try:
        if webdriver_service == None:
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
    printDebug(" Driver Started Sucessfully")
    return driver


def getTranscription(service, url):
    '''
    '''
    i = 0
    print(url)

    if (service == None) or (url == ""):
        return
    
    printDebug("Atempting Load")
    for _ in range(MAX_TRIES):
        try:
            # Load url
            driver = startDriver(service)
            driver.get(url)
            time.sleep(15)

            printDebug(" Loaded Page, finding app..")
            
            # Load app by tag
            app = driver.find_element(By.TAG_NAME, 'ytd-app')
            time.sleep(5)

            printDebug(" Opening Actions Menu")

            # Locate and click actions button
            content = app.find_element(By.ID, 'content')
            pg_mgr = driver.find_element(By.ID, 'page-manager')
            col = pg_mgr.find_element(By.ID, 'columns')
            below = col.find_element(By.ID, 'below')
            actions = below.find_element(By.ID, 'actions')
            button = actions.find_element(By.ID, 'button-shape')
            button.click()
            printDebug("  Action menu clicked")
            break
        except:
            printDebug("Load Failed... " + str(i))
            if driver != None:
                driver.close()
            time.sleep(1)
            pass
    time.sleep(5)

    printDebug(" Locating popup menu")
    # Locate and click transcript button in actions dropdown
    popup = driver.find_element(By.TAG_NAME, 'ytd-popup-container')
    dropdowns = popup.find_elements(By.TAG_NAME, 'tp-yt-iron-dropdown')

    printDebug("  Selecting Show Transcript action")
    transcript_enabled = False
    for dropdown in dropdowns:
        if (dropdown.is_displayed()):
            items = dropdown.find_elements(By.TAG_NAME, 'ytd-menu-service-item-renderer')
            for item in items:
                if "transcript" in item.text:
                    item.click()
                    transcript_enabled = True
                    printDebug("  Transcript enabled")
                    break
            if transcript_enabled:
                break
        
    if not transcript_enabled:
        printDebug("Failed to enable transcript, exiting")
        return
    time.sleep(5)

    printDebug(" Locating Transcript")
    transcript_found = False
    # Download Transcript
    for _ in range(MAX_TRIES):
        try:
            sec = col.find_element(By.ID, 'secondary')
            panels = sec.find_element(By.ID, 'panels')
            sections = panels.find_elements(By.TAG_NAME, 'ytd-engagement-panel-section-list-renderer')
            printDebug(" Secondary Col Panels found")
            for section in sections:
                if "EXPANDED" in section.get_attribute('visibility'):
                    printDebug("  Transcript found and downloaded")
                    transcript_found = True
                    transcript = section.text
                    break
            break
        except:
            time.sleep(1)
            pass
        
    # Check in below Column
    if not transcript_found:
        printDebug("  Transcript not in side column, checking below..")
        for _ in range(MAX_TRIES):
            try:
                panels = below.find_element(By.ID, 'panels')
                sections = panels.find_elements(By.TAG_NAME, 'ytd-engagement-panel-section-list-renderer')
                printDebug("   Primary Col Panels found")
                for section in sections:
                    if "EXPANDED" in section.get_attribute('visibility'):
                        printDebug("   Transcript found and downloaded")
                        transcript_found = True
                        transcript = section.text
                        break
                break
            except:
                time.sleep(1)
                pass
    

    printDebug("Close webdriver")
    # close driver
    driver.close()

    if transcript_found:
        printDebug("Save Transcript")
        # Write transcript to file
        if "watch?v=" in url:
            filename = url.lstrip("https://www.youtube.com/watch?v=") + "_syt.txt"
        elif "https://youtu.be/" in url:
            filename = url.lstrip("https://youtu.be/") + "_syt.txt"
        else:
            filename = 'transcript_syt.txt'

        if (transcript != None):
            outfile = open(out_dir + filename, 'w')
            outfile.write(transcript)
            outfile.close()
        else:
            print("Failed to save Transcript!")

        return transcript
    else:
        print("Could not find Transcript!")


if __name__ == "__main__":
    # Example transcript
    url = "https://youtu.be/0pMxBM3ahwQ"
    out_dir = "/Users/evan/AIJ"

    # Start Service
    service = startService()
    if service != None:
        # Open the Chrome driver
        getTranscription(service, url)



    
