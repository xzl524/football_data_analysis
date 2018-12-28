# coding: utf-8

import pandas as pd
from tqdm import tqdm
import os, sys, bs4, sqlite3
import numpy as np

ALL_STATISTICS = ['goal', 'shoton', 'shotoff', 'foulcommit', 'card', 'cross', 'corner', 'possession']

def extract_event_stats_from_match(match, event):
    """
    Extract event statistics from match table.
    
    Parameters
    ----------
    match:
        Pandas DataFrame, load from Match database in database.sqlite using pandas.
    event:
        str, event type. Available values are defined in ALL_STATISTICS.
    
    Return
    ------
    df:
        Pandas DataFrame, each row represents one event.
    """
    
    df = pd.DataFrame()
    
    # df_partial is used to speed up concat process.
    df_partial = pd.DataFrame() 
    
    match = match[match[event].notnull()]
    
    # loop over each match
    for i in tqdm(np.arange(match.shape[0]), desc='EXTRACTING {} STATS'.format(event.upper()), unit='MATCHES'):        
        
        # create a soup to parse
        soup = bs4.BeautifulSoup(match.iloc[i][event], 'lxml')        
        
        # loop over each event
        for element in soup.find(event).find_all('value', recursive=False):
            element_dict = {}
            for item in element.find_all():
                element_dict[item.name] = item.text
            element_dict['match_api_id'] = match.iloc[i]['match_api_id']

            df_partial = df_partial.append(element_dict, ignore_index=True, sort=True)
            
        if (df_partial.shape[0] >= 50)|(i == (match.shape[0]-1)):
            df = df.append(df_partial, ignore_index=True, sort=True)
            df_partial = pd.DataFrame()
        
    return df

def export_all_stats(database_dir, output_folder, statistics=ALL_STATISTICS):
    """
    Export event stats to csv files.
    
    Parameters
    ----------
    database_dir:
        str, path to database.sqlite.
    output_folder:
        str, path to export. Default is the folder with database.sqlite.
    statistics:
        list, list of events to export. Available event values are defined in ALL_STATISTICS.
        
    Return
    ------
        True
    """

    con=sqlite3.connect(database_dir)
    match = pd.read_sql_query('select * from Match', con)
    
    for event in statistics:
        df = extract_event_stats_from_match(match, event)
        df.to_csv(os.path.join(output_folder, '{}.csv'.format(event)), index=False)
    
    return True

if __name__ == '__main__':
    
    database_dir = sys.argv[1]
    export_all_stats(database_dir, os.path.curdir)