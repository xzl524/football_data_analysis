import os, sys, glob
import pandas as pd
import numpy as np
from tqdm import tqdm
from lxml import etree
from functools import partial
import multiprocessing

sys.path.append('squawka-scraper')

from squawka.utils import SquawkaReport

TIME_SLICE_EVENTS = [
    'action_areas',
    'all_passes',
    'balls_out',
    'blocked_events',
    'cards',
    'clearances',
    'corners',
    'crosses',
    'extra_heat_maps',
    'fouls',
    'goal_keeping',
    'goals_attempts',
    'headed_duals',
    'interceptions',
    'keepersweeper',
    'offside',
    'oneonones',
    'setpieces',
    'tackles',
    'takeons',
]

def group_event_stats(data_folder, statistics=TIME_SLICE_EVENTS):

    # construct team table
    team = pd.read_csv(os.path.join(data_folder, 'teams.csv'))
    # Rename team id column to be consistent with team id column in match event tables
    team = team.rename(columns={'id':'team'})

    for event_type in statistics:
        if (event_type not in ['action_areas', 'players', 'teams', 'oneonones']) and (os.path.isfile(os.path.join(data_folder, '{}.csv'.format(event_type)))):

            event = pd.read_csv(os.path.join(data_folder, '{}.csv'.format(event_type)), low_memory=True)

            if 'team_id' in event.columns:
                event = event.rename(columns={'team_id':'team'})

            # drop records with team=NaN
            event = event.dropna(subset=['team'])
            # transform events into numbers of event for teams 
            event_team =event.groupby(by=['match_id', 'team'], as_index=False).count()[['match_id', 'team', 'competition']]
            event_team = event_team.rename(columns={'competition': event_type})
            # find out all teams shown in matches
            event_team = pd.merge(team[team.match_id.isin(event_team.match_id)], event_team, 
                                  how='left', on=['match_id', 'team'])[['match_id', 'team', '{}'.format(event_type)]]
            event_team = event_team.fillna(0)
            team = pd.merge(event_team, team, how='outer', on = ['match_id', 'team'])
    
    return team

def extract_goal_stats_from_xml(path):

    with open(path, 'r') as f:
        data = f.read()

    xml = etree.fromstring(data)

    report = SquawkaReport(path)
    result = xml.xpath('/squawka/data_panel/system/headline/text()')[0]

    df = pd.DataFrame()

    for i in range(2):
        goal_dict = {}
        goal_dict['team'] = report.teams[i]['id']
        if report.teams[i]['state'] == 'home':
            if len(' '.join(result.split('- ')[0].split(' ')[:-2])) != 0: # correct format
                goal_dict['goals'] = result.split('- ')[0].split(' ')[-2]
            else:
                goal_dict['goals'] = np.nan
        else:
            if len(' '.join(result.split('- ')[1].split(' ')[1:])) != 0:
                goal_dict['goals'] = result.split('- ')[1].split(' ')[0]
            else:
                goal_dict['goals'] = np.nan
        goal_dict['match_id'] = report.match_id

        df = df.append(goal_dict, ignore_index=True)

    return df

def extract_goal_stats_from_xml_folder(xml_folder):
    
    xml_paths = glob.glob(os.path.join(xml_folder, '*.xml'))
    pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)
    partial_loader = partial(extract_goal_stats_from_xml)
    df = pd.concat(pool.imap(partial_loader, xml_paths), axis=0, ignore_index=True)
    df['team'] = df['team'].astype(int)
    df['goals'] = df['goals'].astype(int)

    return df

def merge_teamstats_to_match_table(teamstats):
    
    home_mapping = {i:'home_team_{}'.format(i) for i in TIME_SLICE_EVENTS if i not in ['action_areas', 'oneonones']}
    home_mapping['team'] = 'home_team_id'
    home_mapping['long_name'] = 'home_team'
    home_mapping['goals'] = 'home_team_goals'
    away_mapping = {i:'away_team_{}'.format(i) for i in TIME_SLICE_EVENTS if i not in ['action_areas', 'oneonones']}
    away_mapping['long_name'] = 'away_team'
    away_mapping['team'] = 'away_team_id'
    away_mapping['goals'] = 'away_team_goals'

    home_team = teamstats[teamstats['state']=='home']
    home_team = home_team.rename(columns=home_mapping)
    home_team = home_team[['match_id', 'competition', 'kickoff'] + [home_mapping[key] for key in home_mapping]]

    away_team = teamstats[teamstats['state']=='away']
    away_team = away_team.rename(columns=away_mapping)
    away_team = away_team[['match_id', 'competition', 'kickoff'] + [away_mapping[key] for key in away_mapping]]

    # merge to match table
    match = pd.merge(home_team, away_team, on=['match_id', 'competition', 'kickoff'])
    
    # reorder columns
    col_head = ['match_id', 'competition', 'kickoff', 'home_team_id', 'home_team',
                'away_team_id', 'away_team', 'home_team_goals', 'away_team_goals']
    match = match[col_head + [i for i in match.columns if i not in col_head]]
    
    return match

if __name__ == '__main__':
    team = group_event_stats('out')
    goal = extract_goal_stats_from_xml_folder('data')
    team = pd.merge(team, goal, on=['match_id','team'], how='left')
    team.to_csv(os.path.join('out', 'teamstats.csv'), encoding='utf-8', index=False)

    match = merge_teamstats_to_match_table(team)
    match.to_csv(os.path.join('out', 'matchstats.csv'), encoding='utf-8', index=False)