from acquisition import acquisition
from cleaning import cleaning
from webscraping import webscraping
#from reporting import reporting

def main():
    data = acquisition()
    filtered = cleaning(data)
    enriched = webscraping(filtered)
    #results = plotting_data(enriched)

if __name__ == '__main__':
    main()