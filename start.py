# EVS Project Scraper Version 1.0
# MIT License by Milan Maximilain Mihaldinecz / Rosian.org . Source is available on GitHub.


# Importing libs
import json
import http.client
import datetime
import time
import re
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import sys
import os
from bs4 import BeautifulSoup 

#This connects to one of the search results pages on a specific page number. Returns HTML.
def getOneSearchPage(pagenum=2):

    provider = 'europa.eu'
    req = '/youth/volunteering/project_en?page=' + str(pagenum)

    conn = http.client.HTTPSConnection(provider, 443)
    conn.putrequest('GET', req)
    conn.endheaders()
    resp = conn.getresponse()
    result = resp.read()

    return str(result)

# This connects to one of the project pages. Returns HTML. 
# Requires URL as input like: '/youth/solidarity/placement/12131_en'
def getOneProjectPage(req=""):

    provider = 'europa.eu'
    

    conn = http.client.HTTPSConnection(provider, 443)
    conn.putrequest('GET', req)
    conn.endheaders()
    resp = conn.getresponse()
    result = resp.read()

    return result

#Extracts project page URLs from a search page result string. Returns empty list of no such urls
def extractProjectURLs(htmltext=""):
    result = re.findall('/youth/solidarity/placement/(?:[-\w.]|(?:%[\da-fA-F]{2}))+', htmltext)
    
    return result

#Retrieves all the most recent 90 search result pages (about 800 projects) and their URLs
#MaxPages controls how many pages to get back
def getAllProjectURLs(maxPage = 90, showProgress = True):
    result = []

    for i in range(0,maxPage):
        if(showProgress == True):
            print('Scraping search page: ' + str(i))

        spage = str(getOneSearchPage(i))
        newUrls = extractProjectURLs(spage)
        result = result + newUrls

    return result

#Writes an array to file
def writeToFile(data="", filename=""):

    print('Writing to file: ' + filename)
    with open('output/' + filename, 'w') as f:
        for item in data:
            f.write("%s\n" % item)
            
    return 0

# Writes a string to file (used for the final HTML output)
def writeResultsToHTML(data,filename):
    Html_file = open('output/' + filename,"w")
    Html_file.write(data)
    Html_file.close()
    return 0


#Extracts the project section/text from a HTML of a project page. Returns a string (HTML)
def getProjectPageBody(projPage=""):
    result = ""
    soup = BeautifulSoup(projPage, 'lxml')
    result = soup.find_all("div", class_="region region-content")
    return result[0]

# Retrieves all project pages from the URLs and extracts the main content .This might take long. 
def getAllProjectPagesExtracted(urls, showProgress=True):
    result = []
    urlcount = len(urls)

    i = 0
    for url in urls:
        if(showProgress==True):
            print('Retrieving project '+str(i)+'/'+str(urlcount))
        
        page = getOneProjectPage(url)
        extracted = getProjectPageBody(page)
        result.append(extracted)
        i = i + 1

    return result


#Merges multiple project pages into one very long. Returns as HTML.
#projectBodies is a list of projects (HTML) extracted from other project pages.
def mergeProjectPages(urls, projectBodies):
    result = '<html><body>'
    result = '<h1>Total number of projects: ' + str(len(urls)) + '</h1>'
    i = 0

    for url in urls:
        fullurl = 'https://europa.eu/' + str(url)
        result = result + '<h1>Project ' + str(i) + ': <a target="_blank" href="' + fullurl + '">' + fullurl + '</a></h1>'
        result = result + str(projectBodies[i])
        i = i + 1

    result = result + '</body></html>'

    return str(result)

os.system('clear') #clear console 
listOfLinks = getAllProjectURLs(90,True) #get most recent 900 project urls
writeToFile(listOfLinks, "projectlinks.txt") #save project link urls to disk
listOfProjectPages = getAllProjectPagesExtracted(listOfLinks,True) #Get all the project pages and extracts the project content
mergedresult = mergeProjectPages(listOfLinks, listOfProjectPages) #Merges the projects into one single HTML file
writeResultsToHTML(mergedresult, "allprojects.html") #Writes the merged project file to disk

print("\n Script run finished.")

