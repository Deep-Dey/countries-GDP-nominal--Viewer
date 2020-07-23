# importing the libraries
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

url="https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")

gdp_table = soup.find("table", attrs={"class": "wikitable"})
gdp_table_data = gdp_table.tbody.find_all("tr")

headings = []
for td in gdp_table_data[0].find_all("td"):
    headings.append(td.b.text.replace('\n', ' ').strip())

i=int(input("Press 1 to view GDP details\nPress any key to Store only details as CSV..."))

data = {}
for table, heading in zip(gdp_table_data[1].find_all("table"), headings):

    headers = []
    for th in table.find_all("th"):
        headers.append(th.text.replace('\n', ' ').strip())

    table_data = []
    for tr in table.tbody.find_all("tr"):
        t_row = list()
        for td in tr.find_all("td"):
            t_row.append(td.text.replace('\n', '').strip())
        table_data.append(t_row)

    df = pd.DataFrame(data=table_data, columns=headers)
    df=df[1:]
    df = df.replace(['—'], np.NaN)
    if i==1:
        print(heading)
        print(df)
        choice = input("Do you want to see the details as Bar Chart......(y/n)")
        if choice == 'y':
            n = int(input("For how many countries(According Rank) you want to see the data Sheet..."))
            new_df = df[1:n + 1]

            sns.set_style("ticks")
            plt.figure(figsize=(30, 20))
            plt.barh(new_df['Country/Territory'], new_df['GDP(US$million)'], align='center', color='blue')
            plt.xlabel('GDP Amount', fontsize=15)
            plt.ylabel('Country Name', fontsize=15)
            plt.xticks(fontsize=10, rotation='vertical')
            plt.yticks(fontsize=10)
            plt.title(heading, fontsize=15)

            for index, value in enumerate(new_df["GDP(US$million)"]):
                plt.text(value, index, str(value), fontsize=10)
            plt.show()
    else:
        directory_path = os.path.join(os.getcwd(), 'GDP/')
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        df.to_csv(directory_path + heading+'.csv', index=False)


