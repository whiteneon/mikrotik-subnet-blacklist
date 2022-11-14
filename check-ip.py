#!/usr/bin/env python3
import os, sys, requests, argparse, re, time
#import shutil
import urllib.request
#from http.cookiejar import CookieJar
import http.cookiejar as cookielib
from fileinput import filename
from urllib.parse import urlparse
from colorama import Back, Fore, Style

HE_QUERY="https://bgp.he.net/ip/"
DEBUG=0
HE_COOKIE = ''
USE_COOKIE_JAR = 0

def loadExportedCookie(cookieFile):
    global HE_COOKIE
    strCookie = ''
    lines = open(cookieFile,'r').read().splitlines()
    for eachLine in lines:
        if len(eachLine) > 3:
            if eachLine[0] != '#':
                elements = re.split('\t+',eachLine)
                #print(elements)
                if len(strCookie) > 3:
                    strCookie = strCookie + "; "
                strCookie = strCookie + elements[5] + "=" + elements[6]
                #print(eachLine)
    if DEBUG:
        print(strCookie)
    HE_COOKIE = strCookie

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
            #if (fileName.find('all_packages') != -1) and (EXTRACT_ZIP_FILES == 1):
            #    splitName = os.path.splitext(fileName)
            #    if splitName[1] == ".zip":
            #        try:
            #            shutil.unpack_archive(strDir + "/" + fileName,strDir)
            #            if (DELETE_ZIP_FILES == 1):
            #                os.unlink(strDir + "/" + fileName)
            #        except Exception as e:
            #            eprint("Error unpacking archive!")
            #            eprint("Details: ")
            #            eprint(e)
        except urllib.error.HTTPError:
            eprint("404 Not found for URL:")
            eprint(strUrl)
        #r = requests.get(strUrl, stream=True)
        #with open(strDir + "/" + fileName, 'wb') as f:
        #    for chunk in r.iter_content():
        #        f.write(chunk)
    else:
        wprint(fileName + " already exists, skipping")

def loadCookie():
    global HE_COOKIE
    HE_COOKIE = open('cookie.txt','r').read().splitlines()[0]

def queryIP(ipAddress):
    global HE_QUERY
    global DEBUG
    global USE_COOKIE_JAR
    global HE_COOKIE
    url = HE_QUERY + ipAddress
    if DEBUG:
        print("URL: " + url)
    if USE_COOKIE_JAR:
        cj = cookielib.MozillaCookieJar('cookies-he-net.txt')
        cj.load()
        for cookie in cj:
            # set cookie expire date to 14 days from now
            cookie.expires = time.time() + 14 * 24 * 3600
        if DEBUG:
            print(cj)
    payload={}    
    if USE_COOKIE_JAR:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'connection': 'keep-alive',
            'pragma': 'no-cache',
            'referer': 'https://bgp.he.net/cc',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua': 'Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform':'Windows',
        }
        response = requests.request("GET", url, headers=headers, cookies=cj, data=payload)
    else:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'connection': 'keep-alive',
            'pragma': 'no-cache',
            'referer': 'https://bgp.he.net/cc',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'sec-ch-ua': 'Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform':'Windows',
            'cookie': HE_COOKIE,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
    ipHtml = response.text
    if DEBUG:
        print("Downloaded IP Info!")
    return ipHtml

def main():
    global ipAddress
    global DEBUG
    global HE_COOKIE
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
        loadExportedCookie('cookies-he-net.txt')
        #loadCookie()
        if DEBUG:
            print("IP Address submitted: ",ipAddress)
            print("Loaded cookie: " + HE_COOKIE)
        ipData = queryIP(ipAddress=ipAddress)
        if ipData.find("You have reached your query limit on bgp.he.net"):
            eprint("Query limit reached.....We've been stopped")
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