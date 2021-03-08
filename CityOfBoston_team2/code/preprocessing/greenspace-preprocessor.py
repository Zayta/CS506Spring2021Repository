import pandas as pd
from pandas import DataFrame
import difflib
import re

def import_data(filename):
    data = pd.read_csv(filename, sep=',', usecols = ['SITE_NAME','OWNERSHIP','DISTRICT','ZonAgg','TypeLong','ACRES','ADDRESS','ShapeSTArea','ShapeSTLength'])
    return data

#https://stackoverflow.com/questions/61858903/remove-duplicate-approximate-word-matching-using-fuzzy-python
def similarity_replace(series):

    reverse_map = {}
    diz_map = {}
    for i,s in series.iteritems():
        diz_map[s] = re.sub(r'[^a-z]', '', s.lower())
        reverse_map[re.sub(r'[^a-z]', '', s.lower())] = s

    best_match = {}
    uni = list(set(diz_map.values()))
    for w in uni:
        best_match[w] = sorted(difflib.get_close_matches(w, uni, n=3, cutoff=0.5), key=len)[0]

    return series.map(diz_map).map(best_match).map(reverse_map)

def columnValues(dataframe, columnName):    
    """
    lists all possible values in a particular column
    """
    return list(set(dataframe[columnName].tolist())) 

def output_data(dataframe,path):
    dataframe.to_csv(path)
    return

df = import_data("../../dataset_ignore/open_space.csv")
df['TypeLong'] = similarity_replace(df.TypeLong)
output_data(df,"../../datasets_clean/open_space_sanitized.csv")



