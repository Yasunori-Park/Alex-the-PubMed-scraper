from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import string
import re
import pandas as pd
from pandas import ExcelWriter
from itertools import repeat

#Patch list:
#Ver. 1.0: Alex is created (yay!)
#Ver. 1.1: Alex can now successfully read an author's affiliation if they have >1 affiliation e.g. Rachael
#          A West has affil 1: USYD, affil 2: Westmead. Searching for "sydney" now shows she is affiliated
#          with Sydney whereas before it did not.
#    !     Alex can now correctly predict a hospital affiliation even if PubMed has listed 1 affiliation
#          only on the first author e.g. 20483747 in v.1.0 was predicted ratio of 0.17, now the ratio
#          is correctly 1.00
#Ver. 1.2.0: Alex can now read multiple PMIDs from an excel file, and retrieve results and store them in
#           a new excel sheet.
#   !       Alex can now retrieve titles, journals, publication year, article type, DOI
#   !       Alex now correctly appends original research as "original research"
#   !       Removed "Macau" from list of countries
#Ver. 1.2.1: Alex can now extract Abstracts from PubMed

#Known bugs:
##Currently can only search for "hospital",
#   not including the word in other languages such as in french
#   Countries that are two words e.g. Czech Republic, United States instead of USA, even if they are in
#   the Country list, are not recognized.
# Need to manually check Batch test results to see how it did in extracting information e.g. affiliations
# PMIDs without any authors listed will lead to an error. 
#Need to test:
#How it responds if the author has multiple countries
#Might need to go through official NCBI channels if we want to run this on >50 PMIDs (e-utilities?)

Country = ['Afghanistan',  'Albania',  'Algeria',  'American Samoa',  'Andorra',  'Angola',  'Anguilla',  'Antarctica',  'Antigua and Barbuda',  'Arctic Ocean',  'Argentina',  'Armenia',  'Aruba', 'Ashmore and Cartier Islands',  'Atlantic Ocean',  'Australia',  'Austria',  'Azerbaijan',  'Bahamas',  'Bahrain',  'Baltic Sea',  'Baker Island',  'Bangladesh',  'Barbados',  'Bassas da India',  'Belarus',
     'Belgium',  'Belize',  'Benin',  'Bermuda',  'Bhutan',  'Bolivia',  'Borneo',  'Bosnia and Herzegovina',  'Botswana',  'Bouvet Island',  'Brazil',  'British Virgin Islands',  'Brunei',  'Bulgaria',  'Burkina Faso',  'Burundi',  'Cambodia',  'Cameroon',  'Canada',  'Cape Verde',  'Cayman Islands',  'Central African Republic',  'Chad',  'Chile',  'China',  'Christmas Island',  'Clipperton Island',
     'Cocos Islands',  'Colombia',  'Comoros',  'Cook Islands',  'Coral Sea Islands',  'Costa Rica',  "Cote d'Ivoire",  'Croatia',  'Cuba',  'Curacao',  'Cyprus',  'Czech Republic',  'Democratic Republic of the Congo',  'Denmark',  'Djibouti',  'Dominica',  'Dominican Republic',  'Ecuador',  'Egypt',  'El Salvador',  'Equatorial Guinea',  'Eritrea',  'Estonia',  'Eswatini',  'Ethiopia',  'Europa Island',
     'Falkland Islands (Islas Malvinas)',  'Faroe Islands',  'Fiji',  'Finland',  'France',  'French Guiana',  'French Polynesia',  'French Southern and Antarctic Lands',  'Gabon',  'Gambia',  'Gaza Strip',  'Georgia',  'Germany',  'Ghana',  'Gibraltar',  'Glorioso Islands',  'Greece',  'Greenland',  'Grenada',  'Guadeloupe',  'Guam',  'Guatemala',  'Guernsey',  'Guinea',  'Guinea-Bissau',  'Guyana',  'Haiti',
     'Heard Island and McDonald Islands',  'Honduras',  'Hong Kong',  'Howland Island',  'Hungary',  'Iceland',  'India',  'Indian Ocean',  'Indonesia',  'Iran',  'Iraq',  'Ireland',  'Isle of Man',  'Israel',  'Italy',  'Jamaica',  'Jan Mayen',  'Japan',  'Jarvis Island',  'Jersey',  'Johnston Atoll',  'Jordan',  'Juan de Nova Island',  'Kazakhstan',  'Kenya',  'Kerguelen Archipelago',  'Kingman Reef',  'Kiribati',
     'Kosovo',  'Kuwait',  'Kyrgyzstan',  'Laos',  'Latvia',  'Lebanon',  'Lesotho',  'Liberia',  'Libya',  'Liechtenstein',  'Line Islands',  'Lithuania',  'Luxembourg',  'Madagascar',  'Malawi',  'Malaysia',  'Maldives',  'Mali',  'Malta',  'Marshall Islands',  'Martinique',  'Mauritania',  'Mauritius',  'Mayotte',  'Mediterranean Sea',  'Mexico',  'Micronesia, Federated States of',  'Midway Islands',  'Moldova',
     'Monaco',  'Mongolia',  'Montenegro',  'Montserrat',  'Morocco',  'Mozambique',  'Myanmar',  'Namibia',  'Nauru',  'Navassa Island',  'Nepal',  'Netherlands',  'New Caledonia',  'New Zealand',  'Nicaragua',  'Niger',  'Nigeria',  'Niue',  'Norfolk Island',  'North Korea',  'North Macedonia',  'North Sea',  'Northern Mariana Islands',  'Norway',  'Oman',  'Pacific Ocean',  'Pakistan',  'Palau',  'Palmyra Atoll',  'Panama',
     'Papua New Guinea',  'Paracel Islands',  'Paraguay',  'Peru',  'Philippines',  'Pitcairn Islands',  'Poland',  'Portugal',  'Puerto Rico',  'Qatar',  'Republic of the Congo',  'Reunion',  'Romania',  'Ross Sea',  'Russia',  'Rwanda',  'Saint Barthelemy',  'Saint Helena',  'Saint Kitts and Nevis',  'Saint Lucia',  'Saint Martin',  'Saint Pierre and Miquelon',  'Saint Vincent and the Grenadines',  'Samoa',  'San Marino',
     'Sao Tome and Principe',  'Saudi Arabia',  'Senegal',  'Serbia',  'Seychelles',  'Sierra Leone',  'Singapore',  'Sint Maarten',  'Slovakia',  'Slovenia',  'Solomon Islands',  'Somalia',  'South Africa',  'South Georgia and the South Sandwich Islands',  'South Korea',  'South Sudan',  'Southern Ocean',  'Spain',  'Spratly Islands',  'Sri Lanka',  'State of Palestine',  'Sudan',  'Suriname',  'Svalbard',  'Sweden',  'Switzerland',
     'Syria',  'Taiwan',  'Tajikistan',  'Tanzania',  'Tasman Sea',  'Thailand',  'Timor-Leste',  'Togo',  'Tokelau',  'Tonga',  'Trinidad and Tobago',  'Tromelin Island',  'Tunisia',  'Turkey',  'Turkmenistan',  'Turks and Caicos Islands',  'Tuvalu',  'Uganda',  'Ukraine',  'United Arab Emirates',  'United Kingdom',  'Uruguay',  'USA',  'Uzbekistan',  'Vanuatu',  'Venezuela',  'Viet Nam',  'Virgin Islands',  'Wake Island',  'Wallis and Futuna',
     'West Bank',  'Western Sahara',  'Yemen',  'Zambia',  'Zimbabwe', "UK", "United States", "United States of America", "PRC", "No Country Listed on PubMed"]


def run_Alex(arg="Alex_test.xlsx", example_save_file=r'Alex_scrape_results.xlsx'):
    start_final = time.time()

    #Place all lists to be exported to Excel here
    PMID_column = []
    Title_column = []
    Journal_column = []
    doi_column = []
    Publication_Year_column = []
    Article_Type_column = []
    Affiliation_column = []
    Country_column = []
    Abstract_column = []

    Counter_date = []
    Counter_article_type = []
    Counter_doi = []


    #Read an excel file into the function
    data_frame_from_excel = pd.read_excel(arg)
    list_of_PMID_to_search = data_frame_from_excel["PMID"].to_list()

    #Retrieve the relevant web page for each PMID
    for PMID in list_of_PMID_to_search:
        start = time.time()
        PMID_column.append(PMID)
        print("Version 1.2 of Alex is now searching for details on PMID: _" + str(PMID) + "_")
        url = "https://pubmed.ncbi.nlm.nih.gov/" + str(PMID)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        array = ['This_elem_is_popped']

        #Retrieve the title of the PMID query
        title = soup.find("h1").getText()
        title = title.replace('\n', ' '). \
            replace('                                 ', ''). \
            replace('           ', '')
        Title_column.append(title)
          
        # Retrieve the abstract of the PMID query
        try:
            new_data = soup.find("div", {"class": "abstract-content selected"})
            new_data.strong.decompose()
            Abstract_sections_stripped = new_data.get_text(' ', strip=True)
            Abstract_column.append(Abstract_sections_stripped)
        except AttributeError:
            Abstract_Attr_Error = soup.find("div", {"class": "abstract-content selected"}).get_text(strip=True)
            Abstract_column.append(Abstract_Attr_Error)

        #Retrieve desired values from <meta/>
        Poll = []
        Double_check_Poll = []
        Counter_article_type.append("a")
        Counter_doi.append("b")
        Counter_date.append("c")
        for x in soup.find_all("span"):
            x.unwrap()
        for y in soup.find_all("meta"):
            if y.get("name", None) == "citation_author":
                array.append(' cut ' + y.get("content", None))
            if y.get("name", None) == "citation_author_institution":
                array.append(y.get("content", None))
            if y.get("name", None) == "citation_journal_title":
                Journal_column.append(y.get("content", None))
            if y.get("name", None) == "citation_publication_date":
                Publication_Year_column.append(y.get("content", None))
            if y.get("name", None) == "citation_doi":
                doi_column.append(y.get("content", None))
            if y.get("name", None) == "citation_article_type":
                Article_Type_column.append(y.get("content", None))

        #If meta content is missing, force values in to avoid mismatching details to PMIDs
        if len(Article_Type_column) < len(Counter_article_type):
            Article_Type_column.append("Original research")
        else:
            pass
        if len(doi_column) < len(Counter_doi):
            doi_column.append("No DOI listed")
        else:
            pass
        if len(Publication_Year_column) < len(Counter_date):
            Publication_Year_column.append("No date listed")
        else:
            pass
        #Split affiliations per author
        array = [''.join(letter for letter in word if letter not in
                         string.punctuation) for word in array if word]
        def split_array(s_list: list, substring: str) -> list:
            split_list = list()
            split_list.append(list())
            for line in s_list:
                if substring in line and len(split_list[-1]) != 0:
                    split_list.append(list())
                    continue
                split_list[-1].append(line)
            return split_list
        list_of_lists = split_array(array, ' cut ')
        list_of_lists.pop(0)

        #Within each affiliation search for a given keyword
        def find(list):
            list1_lower = [[j.lower() for j in i] for i in list]
            for each_author in list1_lower:
                new = " ".join(str(x) for x in each_author)
                try:
                    re.search(r'\bhospital\b', new).group(0)
                    Hospital_result = "Yes"
                    Poll.append(Hospital_result)
                except AttributeError:
                    re.search(r'\bhospital\b', new)
                    Hospital_result = "No"
                    Poll.append(Hospital_result)
            total = len(Poll)
            count_Yes = Poll.count('Yes')
            ratio = count_Yes / total
            ratio_2dp = '{0:.2f}'.format(ratio)
            print("-----------------------------------------------------------------------------")
            if ratio >= 0.5:
                print("The ratio of authors affiliated with hospitals vs all authors is: " + str(ratio_2dp) +
                      "\nThis paper is LIKELY to be hospital affiliated")
                Affiliation_column.append("Yes")
            else:
                print("Alex needs to recheck the ratio...just one second!")
                list_lower = [[j.lower() for j in i] for i in list]
                list_lower_without_authors = []
                list_lower_removed_none = []
                for a in list_lower:
                    new = " ".join(str(x) for x in a)
                    lister = [x for x in a if not ' cut ' in new]
                    list_lower_without_authors.append(lister)
                for b in list_lower_without_authors:
                    delete_None_lists = [elem for elem in b if elem is not None]
                    if len(delete_None_lists):
                        list_lower_removed_none.append(delete_None_lists)
                for c in list_lower_removed_none:
                    for d in c:
                        try:
                            text = re.search(r'\bhospital\b', d)
                            if text:
                                Hospital_result = "Yes"
                                Double_check_Poll.append(Hospital_result)
                            else:
                                Hospital_result = "No"
                                Double_check_Poll.append(Hospital_result)
                        except AttributeError:
                            return None
                if len(Double_check_Poll) == 0:
                    Double_check_Poll.append("Yes")
                    Double_check_Poll.extend(repeat("No", 5))
                total_second = len(Double_check_Poll)
                count_Yes_second = Double_check_Poll.count('Yes')
                ratio_second = count_Yes_second / total_second
                ratio_2dp_second = '{0:.2f}'.format(ratio_second)
                if ratio_second >= 0.5:
                    print("The ratio of authors affiliated with hospitals vs all authors is: " +
                          str(ratio_2dp_second) + "\nThis paper is LIKELY to be hospital affiliated")
                    Affiliation_column.append("Yes")
                else:
                    print("The ratio of authors affiliated with hospitals vs all authors is < 0.5."
                          "\nThis paper is UNLIKELY to be hospital affiliated")
                    Affiliation_column.append("No")
        find(list_of_lists)

        #Find the most common Country in affiliations
        def most_frequent(List_country):
            counter = 0
            if len(List_country) == 0:
                List_country.append("No Country Listed on PubMed")
            num = List_country[0]
            for i in List_country:
                curr_frequency = List_country.count(i)
                if (curr_frequency > counter):
                    counter = curr_frequency
                    num = i
            return num
        Country_of_paper = []
        list_lower = [[j.lower() for j in i] for i in list_of_lists]
        for i in range(len(Country)):
            Country[i] = Country[i].lower()
        for x in list_lower:
            list_of_lists_split = [characters for line in x for characters in line.lower().split()]
            if any(words in list_of_lists_split for words in Country):
                l3 = [y for y in list_of_lists_split if y in Country]
                l4 = most_frequent(l3)
                Country_of_paper.append(l4)
        print("Alex believes each author is from: " + str(Country_of_paper) +
              "\nThis paper is likely to be affiliated with: " + most_frequent(Country_of_paper))
        Country_column.append(most_frequent(Country_of_paper))
        #Limit is 3 requests every 1 second. The average script runtime is 1.5.
        #Just to be safe, sleep for 0.35s between runs.
        end = time.time()
        total_time = end-start
        print("This search took: " + str(total_time) + " seconds\n=================================="
                                                       "===========================================")
        time.sleep(0.35)

    #Append lists to a dataframe that will be exported to Excel
    transpose_1 = {"PMID": PMID_column,
         "Title": Title_column,
         "Abstract": Abstract_column,
         "Country": Country_column,
         "Hospital Affiliation": Affiliation_column,
         "Recorded publication date": Publication_Year_column,
         "Journal": Journal_column,
         "Article Type": Article_Type_column,
         "DOI": doi_column}
    df_scrape = pd.DataFrame.from_dict(transpose_1, orient="index")
    df_scrape = df_scrape.transpose()
    writer = ExcelWriter(example_save_file)
    df_scrape.to_excel(writer)
    writer.save()
    end_final = time.time()
    total_time_final = end_final - start_final
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
          + "Running Alex for all listed PMIDs took: " + str(total_time_final) + " seconds\n" +
          "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


#Function is: run_Alex(argument_1, argument_2)
#argument_1 is an .xlsx file, empty EXCEPT for the first column titled "PMID",
# that lists PMIDs to be searched
#argument_2 is a file that doesn't exist yet, that will be made by the function.
# If no name is given, it will automatically be called "Alex_scrape_results.xlsx"
#If using your own argument names e.g. argument 2 is NOT "Alex_scrape_results.xlsx":
# File names need to start with r before the quote i.e. r'This_file_is_for_results.xlsx'
#   r'My_list_of_PMIDs.xlsx'

run_Alex(r'Alex_test_255.xlsx', r'Testing_255.xlsx')
