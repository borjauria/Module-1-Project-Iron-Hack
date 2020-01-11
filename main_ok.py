import pandas as pd
import numpy as np
import sqlite3
import re
import os
import matplotlib.pyplot as plt
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import lxml.html as lh
import matplotlib.pyplot as plt

def main_ok():
    # Create a conection to bbdd throught SQLite
    conex = sqlite3.connect(
        "/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/raw/borjauria.db")

    # Extracts the query data directly to a DataFrame
    personal_info = pd.read_sql_query("SELECT * from personal_info", conex)
    business_info = pd.read_sql_query("SELECT * from business_info", conex)
    rank_info = pd.read_sql_query("SELECT * from rank_info", conex)

    # Preview of data
    df_outer = pd.merge(personal_info, business_info, on='id', how='outer')
    df_the_richests_people = pd.merge(df_outer, rank_info, on='id', how='outer')

    # I change the name of the rows to know
    df_the_richests_people.rename(
        columns={'lastName': 'Last Name', 'age': 'Age', 'Unnamed: 0': 'Unnamed', 'gender': 'Gender', 'country': 'From',
                 'image': 'Photo', 'name': 'Name'}, inplace=True)

    # Replace Values
    df_the_richests_people['Age'] = df_the_richests_people['Age'].str.replace(r"[a-zA-Z]+", '')
    df_the_richests_people['From'] = df_the_richests_people['From'].str.replace(r"USA|USA", 'United States')
    df_the_richests_people['Name'] = df_the_richests_people['Name'].str.replace(r"( \S+)", '')
    df_the_richests_people['Gender'] = df_the_richests_people['Gender'].str.replace(r"[M]", 'Male')
    df_the_richests_people['Gender'] = df_the_richests_people['Gender'].str.replace(r"Maleale", 'Male')
    df_the_richests_people['Gender'] = df_the_richests_people['Gender'].str.replace(r"(^F$)", 'Female')
    df_the_richests_people['worth'] = df_the_richests_people['worth'].str.replace(r"[a-zA-Z]+", '')
    df_the_richests_people['worthChange'] = df_the_richests_people['worthChange'].str.replace(r"[a-zA-Z]+", '')

    # Convert all inside of "Last Name" in lowercase.
    df_the_richests_people['Last Name'] = df_the_richests_people['Last Name'].str.capitalize()

    df_the_richests_people.rename(
        columns={'Unnamed: 0': 'Unnamed', 'Source': 'Source & company', 'worthChange': 'Worth Change',
                 'realTimeWorth': 'Real Time Worth', 'realTimePosition': 'Real Time Position'}, inplace=True)

    # I create a new data frame without 'Real Time Worth column, Unnamed: 0_x, Unnamed: 0_y, Unnamed'.
    df_the_richests_people = df_the_richests_people.drop('Real Time Worth', 1)
    df_the_richests_people = df_the_richests_people.drop('Unnamed: 0_x', 1)
    df_the_richests_people = df_the_richests_people.drop('Unnamed: 0_y', 1)
    df_the_richests_people = df_the_richests_people.drop('Unnamed', 1)

    # New data frame with split value columns from Source & Company
    df_the_richests_people[['Industry', 'Company']] = df_the_richests_people["Source & company"].str.split("==> ",
                                                                                                           expand=True)
    # New data frame without the 'Source & company' column.
    df_the_richests_people = df_the_richests_people.drop('Source & company', 1)

    df_the_richests_people['Name'] = df_the_richests_people['Name'].str.capitalize()

    df_the_richests_people['Last Name'].fillna('none', inplace=True)
    df_the_richests_people['Gender'].fillna('', inplace=True)
    df_the_richests_people['From'].fillna('none', inplace=True)
    df_the_richests_people['Photo'].fillna('none', inplace=True)
    df_the_richests_people['worth'].fillna('none', inplace=True)
    df_the_richests_people['Worth Change'].fillna('none', inplace=True)
    df_the_richests_people['Real Time Position'].fillna('none', inplace=True)
    df_the_richests_people['position'].fillna('none', inplace=True)
    df_the_richests_people['Industry'].fillna('none', inplace=True)
    df_the_richests_people['Company'].fillna('none', inplace=True)

    # Here I change the type of the data
    df_the_richests_people['Age'].replace(to_replace='None', value=-9999, inplace=True)
    df_the_richests_people['Gender'].replace(to_replace='None', inplace=True)
    df_the_richests_people['From'].replace(to_replace='None', inplace=True)
    df_the_richests_people['Age'].fillna(-9999, inplace=True)
    df_the_richests_people = df_the_richests_people.astype({'Age': int})
    df_the_richests_people.loc[df_the_richests_people['Age'] > 100, 'Age'] = 2018 - df_the_richests_people['Age']

    df_the_richests_people['Gender'].replace('', np.nan, inplace=True)
    df_the_richests_people['From'].replace('', np.nan, inplace=True)

    df_the_richests_people = df_the_richests_people.dropna()

    df_the_richests_people['Name'] = df_the_richests_people['Name'] + ' ' + df_the_richests_people['Last Name']

    df_the_richests_people = df_the_richests_people[
        ['id', 'Name', 'Age', 'Gender', 'From', 'Industry', 'Company', 'worth', 'Worth Change', 'Real Time Position',
         'Photo']]

    # Saving the dataframe
    df_the_richests_people.to_csv(
        r'/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_done.csv',
        index=False)

    URL = "https://stats.areppim.com/listes/list_billionairesx19xwor.htm"
    web_text = requests.get(URL).text
    soup = BeautifulSoup(web_text, 'lxml')
    our_table = soup.find_all('div', class_='overflowtable')

    billionaires2 = str(our_table)

    billionaires_split = billionaires2.split('</tr><tr>')

    new_billionaires = billionaires_split[1].rstrip('</td>').lstrip('<td>').split('</td><td>')

    new_billionaires_clean = []

    for item in billionaires_split:
        new_billionaires_clean.append(item.rstrip('</td>').lstrip('<td>').split('</td><td>'))

    cols = ['Rank', 'Name', 'Total net worth $US Billion', 'YTD change $US', 'YTD change %', 'Country', 'Industry']

    df = pd.DataFrame(new_billionaires_clean, columns=cols)

    final_df2 = df.drop([0, 501, 502, 503], axis=0)

    # Import the Clean_Forbes.csv
    df_the_richests_people = pd.read_csv(
        "/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_done.csv")

    # Merge the two dataframes (Forbes and webscrapping)
    df_final = pd.merge(df_the_richests_people, final_df2, on='Name', how='left')

    df_final = df_final[['Real Time Position', 'Name', 'Age', 'Industry_x', 'From', 'Company', 'worth', 'Worth Change']]

    df_final.rename(columns={'Industry_x': 'Industry'}, inplace=True)