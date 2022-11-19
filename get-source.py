from selenium import webdriver
#from selenium.webdriver.chrome.service import Service as ChromeService
#from webdriver_manager.chrome import ChromeDriverManager

# selenium 4 Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
#import codecs
import os, sys

def main():
    os.environ['WDM_LOCAL'] = '1'
    localPath = os.path.curdir
    localPath = os.path.abspath(localPath)
    #print(localPath)
    localPath = localPath + '\.wdm\drivers\geckodriver\win64\0.32\geckodriver.exe'
    #print(localPath)
    #GeckoDriverManager(path = localPath,cache_valid_range=9999).install()
    #sys.exit()
    #Set executable save path
    #ChromeDriverManager(path = r".\\Drivers").install()
    #ChromeDriverManager(version="2.26", cache_valid_range=1).install()
    #set chromedriver.exe path
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    #driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    #driver = webdriver.Chrome(executable_path="C:\chromedriver.exe")
    driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)
    #maximize browser
    #driver.maximize_window()
    #launch URL
    #driver.get("https://bgp.he.net/ip/49.17.16.200")
    driver.get("https://www.whiteneon.com/births/")
    #get file path to save page
    n=os.path.join("C:\\Users\\gbell\\Downloads","ip-test.html")
    #open file in write mode with encoding
    #f = codecs.open(n, "w", "utf-8")
    #obtain page source
    h = driver.page_source
    print("Page Source follows:")
    print(h)
    driver.get("https://www.whiteneon.com/kelsea.jpg")
    j = driver.get_full_page_screenshot_as_base64()
    #print("Base64 encoded data follows:")
    #print(j)
    #write page source content to file
    #f.write(h)
    #f.close()
    #close browser
    driver.quit()
    with open('./retrieved-data/kelsea.jpg.base64','w') as f:
        f.write(j)
    print("Done")

if __name__ == "__main__":
    main()