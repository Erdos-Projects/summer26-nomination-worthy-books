# %%
import numpy as np
import csv
import pandas as pd
from itertools import islice
import json
import missingno as msno
import matplotlib.pyplot as plt
import string

def clean_publishers(publisher):
    # "/" separates an imprint/collection from its parent company, keep only imprint/collection:
    pub = str(publisher).split("/")[0].strip()

    # turn to lowercase
    pub = pub.lower()

    # clean up spelling of common publishers
    common_publishers = ['tor ', 'ace ', 'del rey ', 'doubleday ', 'bloomsbury ', 'orbit ', 'gollancz ', 'daw ', 'harpercollins', 'macmillan', 'simon & schuster']
    for cp in common_publishers:
        if cp in pub:
            # but keep distinction between uk/us/locations
            try:
                location = "(" + pub.split("(")[1]
                # print(cp, location, pub)
            except:
                location = ''
            pub = cp + location


    return pub.replace(' ', '')

# %%
def combine_publishers(pubcolumn, limitnum = 1):
    publisher_counts = pubcolumn.value_counts()

    single_publishers = publisher_counts[publisher_counts < limitnum]

    pubcolumn = pubcolumn.apply(lambda x: 'Other' if x in single_publishers else x)

    return pubcolumn

# %%
def publisher_tidy(pubcolumn):
    pubcolumn = pubcolumn.apply(clean_publishers)
    return combine_publishers(pubcolumn)
