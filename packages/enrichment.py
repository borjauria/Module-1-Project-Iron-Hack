import requests
import pandas as pd
from bs4 import BeautifulSoup

def enrichment(df):
    URL = 'https://stats.areppim.com/listes/list_billionairesx19xwor.htm'
    web_text = requests.get(URL).text
    soup = BeautifulSoup(web_text, 'lxml')
    our_table = soup.find_all('div', class_ = 'overflowtable')
    billionaires2 = str(our_table)
    billionaires_split = billionaires2.split('</tr><tr>')
    new_billionaires = billionaires_split[1].rstrip('</td>').lstrip('<td>').split('</td><td>')
    new_billionaires_clean = []
    for item in billionaires_split:
        new_billionaires_clean.append(item.rstrip('</td>').lstrip('<td>').split('</td><td>'))

    cols = ['Rank', 'Name', 'Total net worth $US Billion', 'YTD change $US', 'YTD change %', 'Country', 'Industry']
    df = pd.DataFrame(new_billionaires_clean, columns=cols)
    final_df2 = df.drop([0,501,502,503],axis=0)

    # Import the Clean_Forbes.csv
    df_the_richests_people = pd.read_csv("/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_done.csv")

    #Merge the two dataframes (Forbes and webscrapping)
    df_final = pd.merge(df_the_richests_people, final_df2, on='Name', how='left')
    df_final = df_final[['Real Time Position','Name','Age','Industry_x','From','Company','worth','Worth Change']]
    df_final.rename(columns={'Industry_x':'Industry'}, inplace=True)

    # Saving the dataframe
    df = df_final.to_csv('/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_final_clean.csv', index=False)
    return df
