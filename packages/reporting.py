colors = ['burlywood', 'yellowgreen', 'gold', 'r', 'orangered', 'mediumvioletred', 'skyblue', 'navy', 'grey', 'black']

df = pd.read_csv('df')

def num_billionaires_per_country(df):
    df['country'].value_counts()[:25].plot(kind='bar', width=0.9, figsize=(20,10), color = colors)
    plt.xlabel('Country (Top 25)')
    plt.ylabel('Number of billionaires')
    plt.title('Number of billionaires per country')
    return plt.savefig('../data/results/billionaires_per_country.png')