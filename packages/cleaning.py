import numpy as np

def wrangling(df):

    df.rename(\
        columns={'lastName': 'Last Name', 'age': 'Age', 'Unnamed: 0': 'Unnamed', 'gender': 'Gender', 'country': 'From', 'image': 'Photo', 'name': 'Name'}, inplace=True)

    # Replace Values
    df['Age'] = df['Age'].str.replace(r"[a-zA-Z]+", '')
    df['From'] = df['From'].str.replace(r"USA|USA", 'United States')
    df['Name'] = df['Name'].str.replace(r"( \S+)", '')
    df['Gender'] = df['Gender'].str.replace(r"[M]", 'Male')
    df['Gender'] = df['Gender'].str.replace(r"Maleale", 'Male')
    df['Gender'] = df['Gender'].str.replace(r"(^F$)", 'Female')
    df['worth'] = df['worth'].str.replace(r"[a-zA-Z]+", '')
    df['worthChange'] = df['worthChange'].str.replace(r"[a-zA-Z]+", '')

    # Convert all inside of "Last Name" in lowercase.
    df['Last Name'] = df['Last Name'].str.capitalize()

    df.rename(columns={'Unnamed: 0': 'Unnamed', 'Source': 'Source & company', 'worthChange': 'Worth Change', 'realTimeWorth': 'Real Time Worth', 'realTimePosition': 'Real Time Position'}, inplace=True)

    # I create a new data frame without 'Real Time Worth column, Unnamed: 0_x, Unnamed: 0_y, Unnamed'.
    df = df.drop('Real Time Worth', 1)
    df = df.drop('Unnamed: 0_x', 1)
    df = df.drop('Unnamed: 0_y', 1)
    df = df.drop('Unnamed', 1)

    # New data frame with split value columns from Source & Company
    df[['Industry', 'Company']] = df["Source & company"].str.split("==> ", expand=True)

    #New data frame without the 'Source & company' column
    df = df.drop('Source & company', 1)

    df['Name'] = df['Name'].str.capitalize()
    df['Last Name'].fillna('none', inplace=True)
    df['Gender'].fillna('', inplace=True)
    df['From'].fillna('none', inplace=True)
    df['Photo'].fillna('none', inplace=True)
    df['worth'].fillna('none', inplace=True)
    df['Worth Change'].fillna('none', inplace = True)
    df['Real Time Position'].fillna('none', inplace=True)
    df['position'].fillna('none', inplace =True)
    df['Industry'].fillna('none', inplace=True)
    df['Company'].fillna('none', inplace=True)

    # Here I change the type of the data
    df['Age'].replace(to_replace='None', value=-9999, inplace=True)
    df['Gender'].replace(to_replace='None', inplace=True)
    df['From'].replace(to_replace='None', inplace=True)
    df['Age'].fillna(-9999, inplace=True)
    df = df.astype({'Age': int})
    df.loc[df['Age'] > 100, 'Age'] = 2018 - df['Age']

    # I want to know how many nulls there are per column to clean
    df.isnull().sum()

    df['Gender'].replace('', np.nan, inplace=True)
    df['From'].replace('', np.nan, inplace=True)

    df = df.dropna()

    df['Name'] = df['Name'] + ' ' + df['Last Name']

    df = df[['id', 'Name', 'Age', 'Gender', 'From', 'Industry', 'Company', 'worth', 'Worth Change', 'Real Time Position', 'Photo']]

    # Saving the dataframe
    data = df.to_csv('/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_done.csv', index=False)
    return data