import matplotlib.pyplot as plt

def plotting_data(df):
    meanW_GDPP = plt.table
    fig = meanW_GDPP.plot(kind='barh', x='Industry', y='From').get_figure()
    plt.xlabel('ratio_MUSD')
    plt.ylabel('countries')
    plt.title(f'TOP - Comparing Billionaries with GDP by Industry')
    plt.grid(True)
    fig.savefig(f'/Users/borjauria/IRONHACK/Ironhack-Module-1-Project---The-best-ever-project/data/results/graphic.jpg')