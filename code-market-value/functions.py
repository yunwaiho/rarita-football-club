from distutils.log import error
import re
import pandas as pd
import unidecode

######################################################################################################################
non_metrics_col = ['Player', 'Nation', 'Pos', 'Squad', 'Age', 'Born', 'League', 'Year']

######################################################################################################################
def clean_names(name):
    def unidecode_names(name):
        return ".".join([unidecode.unidecode(n).lower() for n in name.split(".")])
    
    return re.sub('[^a-zA-Z.]', '', unidecode_names(name))

def pos_to_onehot(df: pd.DataFrame):
    try:
        positions = df.pop('Pos')
    except KeyError:
        return

    positions.fillna('', inplace=True)

    col_DF = positions.apply(lambda x: 1 if "DF" in x else 0)
    col_FW = positions.apply(lambda x: 1 if "FW" in x else 0)
    col_GK = positions.apply(lambda x: 1 if "GK" in x else 0)
    col_MF = positions.apply(lambda x: 1 if "MF" in x else 0)

    df.insert(2, 'GK', col_GK)
    df.insert(2, 'DF', col_DF)
    df.insert(2, 'MF', col_MF)
    df.insert(2, 'FW', col_FW)