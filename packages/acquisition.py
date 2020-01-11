import pandas as pd
import sqlite3

def adquire():

    # Create a conection to bbdd throught SQLite
    conex = sqlite3.connect("/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/raw/borjauria.db")

    # Extracts the query data directly to a DataFrame
    personal_info = pd.read_sql_query("SELECT * from personal_info", conex)
    business_info = pd.read_sql_query("SELECT * from business_info", conex)
    rank_info = pd.read_sql_query("SELECT * from rank_info", conex)

    # Preview of data
    df_outer = pd.merge(personal_info, business_info, on='id', how='outer')
    df_the_richests_people = pd.merge(df_outer, rank_info, on='id', how='outer')

    return df_the_richests_people