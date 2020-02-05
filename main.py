from packages.acquisition import adquire
from packages.cleaning import wrangling
from packages.enrichment import enrichment
#from packages.reporting import plotting_data

def main():
    data = adquire()
    filtered = wrangling(data)
    enriched = enrichment(filtered)
    #results = plotting_data(enriched)

if __name__ == '__main__':
    main()