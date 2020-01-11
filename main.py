from packages.acquisition import adquire
from packages.wrangling import wrangling
from packages.enrichment import enrichment
#from packages.analyzing import analyze

def main():
    data = adquire()
    filtered = wrangling(data)
    #enriched = enrichment(filtered)
    #results = analyze(enriched)

if __name__ == '__main__':
    main()