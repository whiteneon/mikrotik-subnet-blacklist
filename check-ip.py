#!/usr/bin/env python3
from selenium import webdriver
import os, sys, argparse, re, time
#import shutil
import urllib.request
#from http.cookiejar import CookieJar
import http.cookiejar as cookielib
from fileinput import filename
from urllib.parse import urlparse
from colorama import Back, Fore, Style

linuxSystem = 0

if linuxSystem == 1:
    from selenium.webdriver.firefox.options import Options

HE_QUERY="https://bgp.he.net/ip/"
DEBUG=0

def gprint(debugMessage):
    if DEBUG:
        print(Fore.GREEN + debugMessage + Style.RESET_ALL)

def dprint(debugMessage):
    if DEBUG:
        print(Fore.YELLOW + debugMessage + Style.RESET_ALL)

def wprint(warningMessage):
    if DEBUG > 1:
        print(Fore.MAGENTA + warningMessage + Style.RESET_ALL)

def eprint(errorMessage):
    print(Fore.RED + errorMessage + Style.RESET_ALL)
    
def loadStringFromFileInFolder(strDir,strFileName):
    if not strDir[-1] == '/':
        strDir = strDir + '/'
    if os.path.isfile(strDir + strFileName):
        wprint("Reading data from: " + strDir + strFileName)
        try:
            with open(strDir + strFileName,'rb') as f:
                strData = f.read().decode('utf-8')
        except Exception:
            eprint("Error reading data from file:")
            eprint(strFileName)
    else:
        wprint(strFileName + " doesn't exist!")
        strData = None
    return strData

def saveStringToFileInFolder(strData,strDir,strFileName):
    if not strDir[-1] == '/':
        strDir = strDir + '/'
    if not os.path.isdir(strDir):
        os.makedirs(strDir, mode = 0o777, exist_ok = True)
    if not os.path.isfile(strDir + strFileName):
        wprint("saving to: " + strDir)
        try:
            strDataEncoded = strData.encode('utf-8')
            with open(strDir + strFileName,'wb') as f:
                f.write(strDataEncoded)
                #f.writelines(strData)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            eprint("Error writing data to file:")
            eprint(strFileName)
            eprint("Deleting file")
            os.unlink(strDir + strFileName)
            eprint("Encoded data:")
            print(strDataEncoded)
    else:
        wprint(strFileName + " already exists, skipping")

def saveURLToFolder(strUrl,strDir):
    if not os.path.isdir(strDir):
        os.makedirs(strDir, mode = 0o777, exist_ok = True)
    a = urlparse(strUrl)
    fileName = os.path.basename(a.path)
    if not os.path.isfile(strDir + "/" + fileName):
        dprint("Retrieving: " + fileName)
        wprint("url: " + strUrl)
        wprint("saving to: " + strDir)
        try:
            urllib.request.urlretrieve(strUrl,strDir + "/" + fileName)
        except urllib.error.HTTPError:
            eprint("404 Not found for URL:")
            eprint(strUrl)
    else:
        wprint(fileName + " already exists, skipping")

def queryIPSelenium(ipAddress):
    """Uses selenium webdriver to use geckodriver (firefox) to retrieve bgp.he.net
       webpage (passing javascript checks in the process)

    Args:
        ipAddress (string): quad dotted notation of IP address to retrieve info about

    Returns:
        string: source of bgp.he.net web page specific to IP requested
    """
    global HE_QUERY
    global DEBUG
    url = HE_QUERY + ipAddress
    if DEBUG:
        print("URL: " + url)
    os.environ['WDM_LOCAL'] = '1'
    localPath = os.path.curdir
    localPath = os.path.abspath(localPath)
    #print(localPath)
    localPath = localPath + '\.wdm\drivers\geckodriver\win64\0.32\geckodriver.exe'
    #print(localPath)
    if linuxSystem == 1:
        options = Options()
        options.binary_location = r'/mnt/c/Users/gbell/Documents/SourceCode/mikrotik-subnet-blacklist/selenium-stuff/geckodriver'
        #driver = webdriver.Firefox(executable_path=r'C:\WebDrivers\geckodriver.exe', options=options)
        driver = webdriver.Firefox(options=options)
    else:
        driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)
    #maximize browser
    #driver.maximize_window()
    #driver.set_window_size(width=150,height=150)
    #launch URL
    driver.get(url)
    #get file path to save page
    #n=os.path.join("C:\\Users\\gbell\\Downloads","ip-test.html")
    #open file in write mode with encoding
    #f = codecs.open(n, "w", "utf-8")
    driver.save_full_page_screenshot('./retrieved-data/screenshot.png')
    #obtain page source
    h = driver.page_source
    #write page source content to file
    #f.write(h)
    #f.close()
    #close browser
    driver.quit()
    return h
    
def main():
    global ipAddress
    global DEBUG
    parser = argparse.ArgumentParser(description='Find all associated IPs/Networks of IP Address')
    parser.add_argument('--verbose', '-v', action='count', default=0, required=False, help="Enable Debugging")
    parser.add_argument('-i', '--ip', type=str, required=True, help="IP Address to inspect")
    parser.add_argument('-l', '--list', type=str, required=False, help="Create Pasteable RouterOS firewall/address-list script")
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    routerOSList = args.list
    verbosityLevel = args.verbose
    if verbosityLevel > 0:
        print('Verbosity Level: ' + str(verbosityLevel))
        DEBUG=verbosityLevel
    ipAddress = args.ip
    ipData = loadStringFromFileInFolder('./retrieved-data/',ipAddress + '.txt')
    if ipData == None:
        #Saved data doesn't exist, retrieve it and save it
        if DEBUG:
            print("IP Address submitted: ",ipAddress)
        ipData = queryIPSelenium(ipAddress=ipAddress)
        if ipData.find("You have reached your query limit on bgp.he.net") != -1:
            eprint("ERROR: Query limit reached")
            gprint(ipData)
            eprint("Query limit reached.....We've been stopped")
            saveStringToFileInFolder(ipData,'./retrieved-data/','error.txt')
            sys.exit()
        else:
            saveStringToFileInFolder(ipData,'./retrieved-data/',ipAddress + '.txt')
    if verbosityLevel > 4:
        print(ipData)
    #chunks = ipData.split("\n")
    asNumbers = []
    subnets = []
    ipCountry = ''
    orgName = ''
    tabReplacement = ''
    ipData = re.sub('\t+',tabReplacement,ipData)
    chunks = re.split('\n+', ipData)
    if verbosityLevel > 2:
        print(chunks)
    for idx,line in enumerate(chunks):
        if verbosityLevel > 1:
            print(str(idx) + ") " + line)
        if re.match('<td><a href="/AS',line):
            if verbosityLevel > 1:
                print(str(idx) + ") " + line)
            asLines = re.split('>',line)
            for d,asLine in enumerate(asLines):
                if re.match('AS.*<.*',asLine):
                    asNumbers.append(re.split('<',asLine)[0])
                if verbosityLevel > 1:
                    print(str(d) + ") " + asLine)
        if re.match('<a href="/net/',line):
            if verbosityLevel > 1:
                print(str(idx) + ") " + line)
            netLines = re.split('>',line)
            subnets.append(re.split('<',netLines[1])[0])
        if re.match('Organization.*Name',line):
            orgName = re.split(':',line)[1].strip()
        if re.match('country',line.lower()):
            ipCountry = re.split(':',line.upper())[1].strip()
            
    if routerOSList:
        for idx,subnet in enumerate(subnets):
            if ipCountry != '':
                print("add address=" + subnet + " comment=\"Abuser-" + asNumbers[idx] + "," + ipCountry + "\" list=\"" + routerOSList + "\"")
            elif orgName != '':
                print("add address=" + subnet + " comment=\"Abuser-" + asNumbers[idx] + "," + orgName + "\" list=\"" + routerOSList + "\"")
            else:
                print("add address=" + subnet + " comment=\"Abuser-" + asNumbers[idx] + "\" list=\"" + routerOSList + "\"")
        sys.exit()
    if verbosityLevel > 0:
        print("Found AS Number: " + str(asNumbers))
        print("Found subnets: " + str(subnets))
        try:
            print("Found Organization Name: " + orgName)
        except:
            print("No org name found")
        try:
            print("Found IP Country: " + ipCountry)
        except:
            print("No IP Country found")
            
    else:
        print(str(asNumbers) + ',' + ipCountry + ',' + str(subnets))

if __name__ == "__main__":
    main()