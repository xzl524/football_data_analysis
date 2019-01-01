import pandas as pd
import sqlite3
import os

ALL_STATISTICS = ['goal', 'shoton', 'shotoff', 'foulcommit', 'card', 'cross', 'corner', 'possession']
home_mapping = {i:'home_team_{}'.format(i) for i in ALL_STATISTICS if i != 'goal'}
away_mapping = {i:'away_team_{}'.format(i) for i in ALL_STATISTICS if i != 'goal'}

class Preprocessing:
    
    def __init__(self):
        pass
    
    def group_event_stats(self, data_folder, match, statistics=ALL_STATISTICS):
        """
        Group event statistics for each team in each match.

        Parameters
        ----------
        data_folder:
            str, path to data folder.
        match:
            Pandas DataFrame, load from Match database in database.sqlite using pandas.
        statistics:
            list, list of events to export. Available event values are defined in ALL_STATISTICS.
        """

        # construct team table
        # home team
        home_team = match[['match_api_id', 'home_team_api_id']].copy()
        home_team = home_team.rename(columns={'home_team_api_id': 'team'})
        home_team['ishome'] = 1 # home team flag

        # away team
        away_team = match[['match_api_id', 'away_team_api_id']].copy()
        away_team = away_team.rename(columns={'away_team_api_id': 'team'})
        away_team['ishome'] = 0 # away team flag

        # concat together
        team = pd.concat([home_team, away_team], ignore_index=True)

        for event_type in statistics:

            if event_type != 'goal':
                event = pd.read_csv(os.path.join(data_folder, '{}.csv'.format(event_type)), low_memory=False)

                if event_type != 'possession':
                    # drop records with team=NaN
                    event = event.dropna(subset=['team'])

                    # transform events into numbers of event for teams 
                    event_team = event.groupby(by=['match_api_id', 'team'],as_index=False).count()[['match_api_id', 'team', 'id']]
                    event_team = event_team.rename(columns={'id': '{}'.format(event_type)})

                    if event_type == 'corner':
                        # delete 1 mistaken record: match id=530123 has 3 team records, delete team=8472
                        event_team = event_team[~((event_team['match_api_id']==530123)&(event_team['team']==8472))]

                    # find out all teams shown in matches
                    event_team = pd.merge(team[team.match_api_id.isin(event_team.match_api_id)], event_team,
                                          how='left',on=['match_api_id','team'])[['match_api_id','team','{}'.format(event_type)]]

                    event_team = event_team.fillna(0)

                elif event_type == 'possession':
                    event = event.dropna(subset=['homepos', 'awaypos'])
                    pos_team = event.groupby(by=['match_api_id'],as_index=False).mean()[['match_api_id','awaypos','homepos']]

                    # home team possession
                    home_pos = pos_team[['match_api_id','homepos']]
                    home_pos = pd.merge(home_team[home_team.match_api_id.isin(home_pos.match_api_id)], home_pos,
                                        how='left',on=['match_api_id'])[['match_api_id', 'team', 'homepos']]
                    home_pos = home_pos.rename(index=str, columns={'homepos':'{}'.format(event_type)})

                    # away team possession
                    away_pos = pos_team[['match_api_id','awaypos']]
                    away_pos = pd.merge(away_team[away_team.match_api_id.isin(away_pos.match_api_id)], away_pos,
                                        how='left',on=['match_api_id'])[['match_api_id', 'team', 'awaypos']]
                    away_pos = away_pos.rename(index=str, columns={'awaypos':'{}'.format(event_type)})

                    # concat home team and away team together
                    event_team = pd.concat([home_pos, away_pos], ignore_index=True)

                team = pd.merge(event_team, team, how='outer', on = ['match_api_id', 'team'])

        return team

    def merge_teamstats_to_match_table(self, team, match):

        home_team = team[team['ishome']==1]
        home_team = home_team.rename(columns=home_mapping)
        home_team = home_team[[home_mapping[key] for key in home_mapping] + ['match_api_id']]

        away_team = team[team['ishome']==0]
        away_team = away_team.rename(columns=away_mapping)
        away_team = away_team[[away_mapping[key] for key in away_mapping] + ['match_api_id']]

        # merge to match table
        match = pd.merge(match, home_team, on='match_api_id', how='left')
        match = pd.merge(match, away_team, on='match_api_id', how='left')

        return match
    
    def merge_country_name(self, con, match):
        
        country = pd.read_sql_query('select * from Country',con)
        country.columns = ['country_id', 'country']
        match = pd.merge(match, country, on='country_id', how='left')
        
        return match
    
    def merge_league_name(self, con, match):
        
        league = pd.read_sql_query('select * from League',con)
        # Change column names for league table to be ready for merge to match table
        league.columns = ['league_id', 'country_id','league']
        match = pd.merge(match, league[['league_id','league']], on='league_id', how='left')
        
        return match
    
    def merge_team_name(self, con, match):
        
        team = pd.read_sql_query('select * from Team',con)
        home_team = team.copy()
        home_team.columns = ['id','home_team_api_id','home_team_fifa_api_id','home_team','home_team_short_name']
        match = pd.merge(match, home_team[['home_team_api_id','home_team']], on='home_team_api_id', how='left')

        away_team = team.copy()
        away_team.columns = ['id','away_team_api_id','away_team_fifa_api_id','away_team','away_team_short_name']
        match = pd.merge(match, away_team[['away_team_api_id','away_team']], on='away_team_api_id', how='left')
        
        return match
    
if __name__ == '__main__':
    prep = Preprocessing()
    con=sqlite3.connect(os.path.join(os.path.curdir, 'database.sqlite'))
    match = pd.read_sql_query('select * from Match', con)
    team = prep.group_event_stats(os.path.curdir, match)
    match = prep.merge_teamstats_to_match_table(team, match)
    match = prep.merge_country_name(con, match)
    match = prep.merge_league_name(con, match)
    match = prep.merge_team_name(con, match)
    match.to_csv(os.path.join(os.path.curdir, 'match.csv'), index=False)