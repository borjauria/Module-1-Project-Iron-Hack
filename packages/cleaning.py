#Create a conection to bbdd throught SQLite
conex = sqlite3.connect("/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/raw/borjauria.db")

#Extracts the query data directly to a DataFrame
personal_info = pd.read_sql_query("SELECT * from personal_info", conex)
business_info = pd.read_sql_query("SELECT * from business_info", conex)
rank_info = pd.read_sql_query("SELECT * from rank_info", conex)
df_outer = pd.merge(personal_info, business_info, on='id', how='outer')
df = pd.merge(df_outer, rank_info, on='id', how='outer')

#Here I change the name of the columns.
def change_name_cols(df, dic):
    for k, v in dic.items():
        df[k] = df[k].str.replace(k,v)
    return df

#Here I eliminate the columns I don't need.
def drop_columns(df, lst):
    for i in lst:
        df.drop(i, axis = 1, inplace=True)
    return df

#With this function I convert the all the words inside of lst in lowercase.
def column_lower(df, lst):
    for i in lst:
        df.update(df[i].str.title())
    return df

#With this function I convert the first letter of the words inside of lst in Uppercase.
def column_upper(df, lst):
    for i in lst:
        df.update(df[i].str.capitalize())
    return df

#With this function I will fill with the word 'Delete' all those cells that do not contain any data.
def fill_none(df, lst):
    for i in lst:
        df.update(df[i].fillna('NaN', inplace=True))
    return df

#Converts all the cells in the list columns to floats
def to_float(df, lst):
    for i in lst:
        df[i] = df[i].astype(float)
    return df

#I split the column 'Source' into two columns ('Industry', 'Company')
df[['Industry', 'Company']] = df['Source'].str.split(' ==> ', expand=True)

#Change_name_cols
df.rename(columns={'lastName':'Last Name', 'age': 'Age', 'Unnamed: 0': 'Unnamed', 'gender': 'Gender', 'country': 'From', 'name': 'Name','realTimePosition': 'Real Time Position'}, inplace=True)

#Replace some values
df['Age'] = df['Age'].str.replace(r"[a-zA-Z]+",'')
df['From'] = df['From'].str.replace(r"USA|USA",'United States')
df['Name'] = df['Name'].str.replace(r"( \S+)",'')
df['Gender'] = df['Gender'].str.replace(r"[M]",'Male')
df['Gender'] = df['Gender'].str.replace(r"Maleale",'Male')
df['Gender'] = df['Gender'].str.replace(r"(^F$)",'Female')
df['worth'] = df['worth'].str.replace(r"[a-zA-Z]+",'')
df['worthChange'] = df['worthChange'].str.replace(r"[a-zA-Z]+",'')

# Convert all inside of all columns in lowercase
low_cols = ['Name', 'Last Name','Gender','From']
column_lower(df, low_cols)

#column_upper
up_cols = ['Name', 'Last Name', 'Company']
column_upper(df, up_cols)

#drop_columns
columns_to_drop = ['id', 'Unnamed: 0_x', 'Source', 'image', 'Unnamed: 0_y', 'Unnamed', 'position','worthChange','realTimeWorth']
drop_columns(df, columns_to_drop)

#columns_to_fill
columns_to_fill = ['Last Name','Gender','From']
fill_none(df, columns_to_fill)

#Change the numbers in list in a float
to_float(df, ['worth', 'Real Time Position'])

df['Age'].replace(to_replace='None',value=-9999, inplace=True)
df['Gender'].replace(to_replace='None', inplace=True)
df['From'].replace(to_replace='None', inplace=True)
df['Age'].fillna(-9999, inplace=True)
df = df.astype({'Age':int})
df.loc[df['Age']> 100, 'Age'] = 2018 - df['Age']
df['Name'] = df['Name'] + ' ' + df['Last Name']
df = df[['Name', 'Age', 'Gender', 'From', 'Real Time Position', 'Industry', 'Company']]
df = df.dropna()

# Saving the dataframe to csv
data = df.to_csv(r'/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/processed/borjauria_done.csv', index=False)