def acquisition():
    #Create a conection to bbdd throught SQLite
    conex = sqlite3.connect("/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/raw/borjauria.db")
    #Extracts the query data directly to a DataFrame
    personal_info = pd.read_sql_query("SELECT * from personal_info", conex)
    business_info = pd.read_sql_query("SELECT * from business_info", conex)
    rank_info = pd.read_sql_query("SELECT * from rank_info", conex)
    df_outer = pd.merge(personal_info, business_info, on='id', how='outer')
    df = pd.merge(df_outer, rank_info, on='id', how='outer')
    return df.to_csv(file)

    return df