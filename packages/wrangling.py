import numpy as np

def wrangling(df_the_richests_people):

    df_the_richests_people.rename(\
        columns={'lastName': 'Last Name', 'age': 'Age', 'Unnamed: 0': 'Unnamed', 'gender': 'Gender', 'country': 'From', 'image': 'Photo', 'name': 'Name'}, inplace=True)

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

    df_the_richests_people.rename(\
        columns={'Unnamed: 0': 'Unnamed', 'Source': 'Source & company', 'worthChange': 'Worth Change', 'realTimeWorth': 'Real Time Worth', 'realTimePosition': 'Real Time Position'}, inplace=True)

    # I create a new data frame without 'Real Time Worth column, Unnamed: 0_x, Unnamed: 0_y, Unnamed'.
    df_the_richests_people = df_the_richests_people.drop('Real Time Worth', 1)
    df_the_richests_people = df_the_richests_people.drop('Unnamed: 0_x', 1)
    df_the_richests_people = df_the_richests_people.drop('Unnamed: 0_y', 1)
    df_the_richests_people = df_the_richests_people.drop('Unnamed', 1)

    # New data frame with split value columns from Source & Company
    df_the_richests_people[['Industry', 'Company']] = df_the_richests_people["Source & company"].str.split("==> ", expand=True)

    #New data frame without the 'Source & company' column
    df_the_richests_people = df_the_richests_people.drop('Source & company', 1)

    df_the_richests_people['Name'] = df_the_richests_people['Name'].str.capitalize()
    df_the_richests_people['Last Name'].fillna('none', inplace=True)
    df_the_richests_people['Gender'].fillna('', inplace=True)
    df_the_richests_people['From'].fillna('none', inplace=True)
    df_the_richests_people['Photo'].fillna('none', inplace=True)
    df_the_richests_people['worth'].fillna('none', inplace=True)
    df_the_richests_people['Worth Change'].fillna('none', inplace = True)
    df_the_richests_people['Real Time Position'].fillna('none', inplace=True)
    df_the_richests_people['position'].fillna('none', inplace =True)
    df_the_richests_people['Industry'].fillna('none', inplace=True)
    df_the_richests_people['Company'].fillna('none', inplace=True)

    # Here I change the type of the data
    df_the_richests_people['Age'].replace(to_replace='None', value=-9999, inplace=True)
    df_the_richests_people['Gender'].replace(to_replace='None', inplace=True)
    df_the_richests_people['From'].replace(to_replace='None', inplace=True)
    df_the_richests_people['Age'].fillna(-9999, inplace=True)
    df_the_richests_people = df_the_richests_people.astype({'Age': int})
    df_the_richests_people.loc[df_the_richests_people['Age'] > 100, 'Age'] = 2018 - df_the_richests_people['Age']

    # I want to know how many nulls there are per column to clean
    df_the_richests_people.isnull().sum()

    df_the_richests_people['Gender'].replace('', np.nan, inplace=True)
    df_the_richests_people['From'].replace('', np.nan, inplace=True)

    df_the_richests_people = df_the_richests_people.dropna()

    df_the_richests_people['Name'] = df_the_richests_people['Name'] + ' ' + df_the_richests_people['Last Name']

    df_the_richests_people = df_the_richests_people[['id', 'Name', 'Age', 'Gender', 'From', 'Industry', 'Company', 'worth', 'Worth Change', 'Real Time Position', 'Photo']]

    # Saving the dataframe
    data = df_the_richests_people.to_csv('/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_done.csv', index=False)
    return data