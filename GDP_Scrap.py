# importing the libraries
from bs4 import BeautifulSoup
import requests
import csv
import os

url="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")
# print(soup.prettify()) # print the parsed data of html

# for link in soup.find_all("a"):
#     print("Inner Text: {}".format(link.text))
#     print("Title: {}".format(link.get("title")))
#     print("href: {}".format(link.get("href")))

gdp_table = soup.find("table", attrs={"class": "wikitable"})
gdp_table_data = gdp_table.tbody.find_all("tr")  # contains 2 rows

# Get all the headings of Lists
headings = []
for td in gdp_table_data[0].find_all("td"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.b.text.replace('\n', ' ').strip()) 
# print(headings)

data = {}
for table, heading in zip(gdp_table_data[1].find_all("table"), headings):
    # Get headers of table i.e., Rank, Country, GDP.
    
    table_data = []
    for tr in table.tbody.find_all("tr"): # find all tr's from table's tbody
        t_row = []
        # Each table row is stored in the form of
        # t_row = {'Rank': '', 'Country/Territory': '', 'GDP(US$million)': ''}

        # find all td's(3) in tr and zip it with t_header
        for td in tr.find_all("td"): 
            t_row.append(td.text.replace('\n', '').strip())
        table_data.append(t_row)

    # Put the data for the table with his heading.
    data[heading] = table_data

i=int(input("Press 1 to view GDP\nPress any key to Store details as CSV..."))
print()
if i==1:
    for topic, table in data.items():
        print(topic)
        headers = [ "Country/Territory", "GDP(US$million)", "Rank" ]
        print(headers)
        for row in table:
            if(row):
                print(row)
        print()
    
for topic, table in data.items():
    directory_path = os.path.join(os.getcwd(), 'OUTPUT/')
    if not os.path.exists(directory_path):
                os.mkdir(directory_path)
                
    # Create csv file for each table
    with open( directory_path + topic + '.csv', 'w',  newline='') as out_file:
        # Each 3 table has headers as following
        headers = [ "Country/Territory", "GDP(US$million)", "Rank" ] # == t_headers
        writer = csv.writer(out_file)
        writer.writerow(headers)
        for row in table:
            if(row):
                writer.writerow(row)

