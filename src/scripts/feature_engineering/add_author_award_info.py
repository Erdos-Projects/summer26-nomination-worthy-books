# %%
import numpy as np
import csv
import pandas as pd
from itertools import islice
import json
import matplotlib.pyplot as plt

from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[1]

dataset_file = REPO_ROOT / 'data' / 'final_book_dataset_cleaned.csv'


# %%
books = pd.read_csv(dataset_file, sep = '\t',
        dtype={
            'author_birthyear' : 'Int64',
            'title_id' : 'Int64',
            'isbn' : 'str'
        }
    )

# %%
books.head(5)

# %%
## add month of publication column, 00 means only year is known
books['month_of_publication'] =books['release_date'].str[5:7].str.replace('00','Unknown')
books.sample(50)

# %%
## Add age of author at publication
books['Author_Age_at_Publication'] = 'Unknown'
books['Author_Age_at_Publication'] = books['Author_Age_at_Publication'].case_when([(books['author_birthyear'].isna() == False,books['release_year'] - books['author_birthyear'])])

# %%
books.sample(15)

# %%
## Add column with number of hugo or locus awards won prior to that date
books['Hugo_Awards_Previously']= books.groupby(['author'])['hugo'].cumsum()
books['Locus_Awards_Previously']= books.groupby(['author'])['locus'].cumsum()

# %%
# display(books[books['author'] == 'Ada Palmer'])
#From the above example we see that .cumsum method counts the current row as well and is causing leakage.

# %%
##Once you run this cell the above bug will be fixed.

## Add column with number of hugo or locus awards won prior to that date
## We do this to ensure that hugo info about current year is not included
# cumsum includes the current year as well

books['Hugo_Awards_Previously'] = (
    books.groupby('author')['hugo'].cumsum() - books['hugo']
)
books['Locus_Awards_Previously'] = (
    books.groupby('author')['locus'].cumsum() - books['locus']
)

# %%
# display(books[books['author'] == 'Ada Palmer'])
#bug fixed

# %%
books.sample(15)

# %%
## Add column with boolean if author been nominated for Hugo/Locus prior to that date
books['Hugo_Nominee_Before'] = 'False'
books['Hugo_Nominee_Before'] = books['Hugo_Nominee_Before'].case_when([(books['Hugo_Awards_Previously'] > 0,True)])
books['Locus_Nominee_Before'] = 'False'
books['Locus_Nominee_Before'] = books['Locus_Nominee_Before'].case_when([(books['Locus_Awards_Previously'] > 0,True)])

# %%
books.sample(100)

# %%
## Add Author Birthplace by country
replace_dict = {'Austria':['Austria-Hungary','Austro-Hungarian Empire','Austria'],
               'Russia':['Russian Empire','Russia','USSR','Soviet'],
               'Germany':['German Empire','Reich','Confederation','Germany','Prussia'],
               'Nigeria':['Nigeria'],
               'India':['INdia','India'],
               'Peru':['Perú','Peru'],
               'Ceylon':['Ceylon'],
               'Papua New Guinea':['Netherlands New Guinea'],
               'Hong Kong':['Territory','Kong','Hong Kong','Komg'],
               'Dominican Republic':['Dominican Republic'],
               'Bailiwack of Jersey':['Balliwack of Jersey','Bailiwick of Jersey'],
               'Trinidad and Tobago':['Tobago','Trinidad'],
               'UK': ['Yorkshire','Wales','England','United Kingdom','UK','Scotland','Northern Ireland','Guernsey','Britain'],
               'Australia':['Sydney','New South Wales','Australia','Queensland','Victoria','Gold Coast'],
               'USA':['Philadelphia','MO','PA','WA','PR','Baltimore','USA','US Virgin Islands','Puerto Rico'],
               'Panama':['Canal Zone','Panama'],
               'Sri Lanka': ['Lanka'],
               'New Zealand':['Zealand','NZ'],
               'East Indies' :['East Indies'],
                'West Indies' :['West Indies','Antilles','Dominica'],
                'El Salvador' :['El Salvador'],
                'South Africa' :['Cape Colony','Pretoria','Port Elizabeth','South Africa','Orange Free'],
                'United Arab Emirates' :['United Arab Emirates'],
                'Sierra Leone' :['Sierra Leone'],
                'Canada': ['British North America','Canada','Alberta'],
                'Guyana':['Guyana','British Guiana'],
                'Cayman Islands': ['Cayman'],
                'Marshall Islands':['Marshall'],
                'Thailand': ['Thailand','Siam'],
                'Malaysia':['Malaya','Malaysia'],
                'Philipines':['Philipines','Philippine Islands'],
                'Ireland' : ['Ireland','Irish'],
                'Turkey':['Turkey','Ottoman Empire'],
                'Rhodesia':['Rhodesia'],
                'Bermuda':['Bermuda'],
                'Kenya':['Kenya'],
                'Jamaica':['Jamaica'],
                'Sweden':['Sweden','Swedish'],
                'Singapore':['Singapore'],
                'Nyasaland':['Nyasaland'],
                'Palestine':['Palestine'],
                'Fiji':['Fiji'],
                'Holy Roman Empire':['Holy Roman Empire'],
                'Myanmar':['Burma','Myanmar'],
                'Malta':['Malta'],
                'Czech Republic':['Czech'],
                'Rwanda':['Rwanda','Portugese West Africa','Kamundongo']
}

def replace_author_birthplace_country(x):
    if pd.isna(x):
        return 'Unknown'
    for country, birthplace in replace_dict.items():
        if any(word in x for word in birthplace):
            return country
    if x not in replace_dict.items():
        return x.strip().split()[-1]
    return x



# %%
books = books.assign(author_birthplace_country=books['author_birthplace'].apply(replace_author_birthplace_country))
books.sample(15)

# %%
## Author Birthplace by continent
continent_dict = {
'Africa' : ['Africa','Zambia','Libya','Sudan','Ethiopia','Madagascar','Morocco','Sudan','Namibia','Niger','Botswana','Liberia','Tunisia','Mauritius',
          'Nyasaland','Sierra Leone','Guinea','Tanzania','Zimbabwe','Uganda','Ghana','Egypt','Kenya','Rwanda','Nigeria','Rhodesia','South Africa',
          ],
'Europe' : ['Cyprus','Marino','Macedonia','Latvia','Holy Roman Empire','Luxembourg','Gibraltar','Bulgaria','Ukraine','Serbia','Bailiwack of Jersey',
          'Denmark','Norway','Iceland','Czech Republic','Greece','Hungary','Finland','Spain','Romania','Malta','Belgium','Poland','Portugal',
          'Switzerland','Yugoslavia','Austria','Sweden','Italy','Netherlands','France','Russia','Germany','Ireland','UK'],
'South America' : ['Suriname','Uruguay','Bolivia','Colombia','Guyana','Chile','Ecuador','Peru','Argentina','Brazil','Venezuela'],
'Central/North America' : ['USA','Honduras','Bahamas','Guatemala','Barbados','Cayman Islands','Croatia','Grenada','Panama','Jamaica','Bermuda',
                         'Haiti','Trinidad and Tobago','Cuba','West Indies','Mexico','Dominican Republic','Canada'],
'Asia' : ['Iraq','East Indies','Myanmar','Philippines','Brunei','Macau','Kuwait','Nepal','United Arab Emirates','Bahrain','Vietnam','Laos','Arabia',
        'Pakistan','Palestine','Sri Lanka','Bangladesh','Persia','Turkey','Lebanon','Ceylon','Korea','Thailand','Indonesia','Taiwan','Iran',
        'Singapore','Malaysia','Philippines','Hong Kong','China','Israel','Japan','India'],
'Oceania' : ['Australia','New Zealand','Samoa','Marshall Islands','Papua New Guinea','Fiji']
}

def replace_author_birthplace_continent(x):
    if pd.isna(x):
        return 'Unknown'
    for country, birthplace in continent_dict.items():
        if any(word in x for word in birthplace):
            return country
    if x not in replace_dict.items():
        return x.strip().split()[-1]
    return x

# %%
books = books.assign(author_birthplace_continent=books['author_birthplace'].apply(replace_author_birthplace_continent))
books.sample(15)

# %%
books.reset_index()


output_file = REPO_ROOT / 'data' / 'data_with_author_and_awards.csv'

books.to_csv(output_file, index = False)


# %%



