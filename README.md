# Alex the PubMed Scraper
A scraper (called **Alex**) for PubMed *(does not use E-utilities yet)* that when fed a list of PMIDs in an excel spreadsheet, returns the following: 
* **PMID**
* **Title** of queried PMID
* **Journal** of queried PMID
* **Publication date** (according to PubMed) of queried PMID
* **Country** the majority of authors are affiliated with of queried PMID
* Whether or not the majority of authors are **affiliated with a hospital** 
* **DOI** of the queried PMID 
* **Article type** of the queried PMID (if listed. If it is blank in the results, it is an original contribution)

Any libraries that are needed to run Alex are listed at the top of the .py file. 

Future updates will include routing the query through E-utilities instead of PubMed. 

## Alex was tested on a list of 255 PubMed IDs:
* Tested PMIDs are stored in: **Alex_test_255.xlsx**
* Results of the PMIDs are stored in: **Testing_255.xlsx**
* Alex took **578 seconds (~9 minutes 38 seconds)** to search the 255 PMIDs (this includes the time.sleep(1) run on all 255 loops)
* Manually rechecking all entries took **1 hour 56 minutes** 
* Of the **n=255** PMIDs, only **n=5** PMIDs didn't have their country correctly extracted
* **n = 1** PMID didn't have their date extracted 
* **n=255** Titles, Hospital Affiliations (calculated by majority), Journal, Article Type and DOI were correctly extracted

