# evs-scraper
Python script to scrape European Voluntary Services ( EVS ) projects.

# Motivation
European Voluntary Services is an amazing opportunity to volunteer abroad. Unfortunately, the user interface provided that allows searching these projects is suboptimal. This script was created to help those who want to find their dream volunteer project.

You can find volunteering opportunities on the EVS portal: https://europa.eu/youth/volunteering/project_en

# What it does
1. It scrapes https://europa.eu/youth/volunteering/project_en pages for available projects
2. Saves the URLs of the project pages into a text file
3. Scrapes all the project pages individually and extracts the main content (no header or footer)
4. Combines the extracted project pages into one single HTML file and writes it to the disk

You can use the extracted file to do searches manually (e.g. ctrl+f) or further transform the data. 
It is already more convenient to read one file as opposed to open all the small pages

Examples:
See the "output" folder for the link file and combined HTML file.


# Requirements
You will need Python 3.6 or newer to run this script (including the BeautifulSoup library)

