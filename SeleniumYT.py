'''

Selenium Youtube Transcriber

'''

import sys
import time

if "selenium" in sys.modules.keys():
    import selenium
    print(selenium.version)

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By

MAX_TRIES = 1000

webdriver_service = service.Service("C:/Users/Evan/Downloads/chromedriver_win32/chromedriver.exe")
webdriver_service.start()
options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', True)
options.add_argument("--window-size=2560,1440")




def getTranscription(url):
    """
    """
    driver = webdriver.Remote(webdriver_service.service_url, options=options)

    i = 0
    while i < MAX_TRIES:
        try:
            # Load url
            driver.get(url)
            time.sleep(10)

            # Load app by tag
            app = driver.find_element(By.TAG_NAME, 'ytd-app')

            # Locate and click actions button
            content = app.find_element(By.ID, 'content')
            pg_mgr = driver.find_element(By.ID, 'page-manager')
            col = pg_mgr.find_element(By.ID, 'columns')
            below = col.find_element(By.ID, 'below')
            actions = below.find_element(By.ID, 'actions')
            button = actions.find_element(By.ID, 'button-shape')
            button.click()
            break
        except:
            time.sleep(1)
            pass
    time.sleep(5)

    # Locate and click transcript button in actions dropdown
    popup = driver.find_element(By.TAG_NAME, 'ytd-popup-container')
    dropdowns = popup.find_elements(By.TAG_NAME, 'tp-yt-iron-dropdown')

    for dropdown in dropdowns:
        if (dropdown.is_displayed()):
            items = dropdown.find_elements(By.TAG_NAME, 'ytd-menu-service-item-renderer')
            for item in items:
                if "transcript" in item.text:
                    item.click()
                    break
            break
    time.sleep(5)

    # Download Transcript
    i = 0
    while i < MAX_TRIES:
        try:
            sec = col.find_element(By.ID, 'secondary')
            panels = sec.find_element(By.ID, 'panels')
            sections = panels.find_elements(By.TAG_NAME, 'ytd-engagement-panel-section-list-renderer')

            for section in sections:
                if "EXPANDED" in section.get_attribute('visibility'):
                    transcript = section.text
                    break
            break
        except:
            time.sleep(1)
            pass

    # Write transcript to file
    if "watch?v=" in url:
        filename = url.lstrip("https://www.youtube.com/watch?v=") + "_syt.txt"
    else:
        filename = 'transcript_syt.txt'
        
    outfile = open(filename, 'w')
    outfile.write(transcript)
    outfile.close()

    # Close web driver
    driver.close()

    return transcript


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=FV7pW4p60VI"
    getTranscription(url)
