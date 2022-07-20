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

## Any results from Alex should be manually checked
Alex has only been tested on the following PMIDs:

* 29046142
* 28771186
* 29151973
* 33279761
* 31376328
* 29467857
* 25721211
* 33843511
* 35022248

Therefore, any further attempts at using Alex should be accompanied with manual rechecking of results. 
