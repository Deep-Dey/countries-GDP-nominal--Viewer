# importing the libraries
from bs4 import BeautifulSoup
import requests
import csv
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

##########################################################################  Scrap
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
##########################################################################################   Export to CSV
i=int(input("Press 1 to view GDP and store as CSV\nPress any key to Store only details as CSV..."))
print()

for topic, table in data.items():
    directory_path = os.path.join(os.getcwd(), 'OUTPUT/')
    if not os.path.exists(directory_path):
                os.mkdir(directory_path)
                
    # Create csv file for each table
    with open(directory_path+topic + '.csv', 'w',  newline='') as out_file:
        # Each 3 table has headers as following
        headers = ["Rank", "Country/Territory", "GDP(US$million)"] # == t_headers
        writer = csv.writer(out_file)
        writer.writerow(headers)
        for row in table:
            if(row):
                writer.writerow(row)
#######################################################################   Use panda to show in a table
    if i == 1:
        print(topic)
        df=pd.read_csv(directory_path+topic + '.csv', encoding="ISO-8859-1")
        new_df = df.replace([''], np.NaN)
        print(new_df)
#######################################################################
        choice=input("Do you want to see the details as Bar Chart......(y/n)")
        if choice=='y':
            n=int(input("For how many countries you want to see the data Sheet..."))
            new_df=new_df[1:n+1]

            sns.set_style("ticks")
            plt.figure(figsize=(30, 20))
            plt.barh(new_df['Country/Territory'], new_df['GDP(US$million)'], align='center', color='blue')
            plt.xlabel('GDP Amount', fontsize=15)
            plt.ylabel('Country Name', fontsize=15)
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)
            plt.title(topic, fontsize = 15 )

            for index, value in enumerate(new_df["GDP(US$million)"]):
                plt.text(value, index, str(value), fontsize=10)
            plt.show()


