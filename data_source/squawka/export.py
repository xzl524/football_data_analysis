import sys
sys.path.append('squawka-scraper')

from squawka.utils import export_all_stats

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
    'takeons'
]

ALL_STATISTICS = sorted(TIME_SLICE_EVENTS+['teams','players'])

if __name__ == '__main__':
    export_all_stats('data/', 'out/', ALL_STATISTICS, convert=False)