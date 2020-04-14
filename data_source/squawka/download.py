import os
import glob
from urllib2 import urlopen, Request
from tqdm import tqdm

ALL_LEAGUES = ['epl', 'eredivisie', 'seriea', 'ligue1', 'laliga', 'bliga', 'championship', 'rpl', 'mls',
               'brasil-serie-a', 'liga-mx', 'a-league', 'turkish-super-lig', 'primeira-liga', 'euro-cup',
               'europa-league', 'champions-league', 'world-cup'
              ]

def download_xmls(xml_dir, match_id_range, comp=None):
    """
    Directly download xmls from Squawka.

    Parameters
    ----------
    xml_dir: str, path to xml folder.
    match_id_range: list or iterator, range of match ids to search for xmls.
    Example: range(40000).
    """

    def look_for_league(match_id):
        """
        Look for league name for a given match id if any.

        Parameters
        ----------
        match_id, int, greater than 0.

        Returns
        -------
        comp: league name if any. If no, return None.
        """

        user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

        for comp in ALL_LEAGUES:
            url = "http://s3-irl-{}.squawka.com/dp/ingame/{}".format(comp, match_id)
            req = Request(url, headers=user_agent)
            try:
                contents = urlopen(req, timeout=3).read()
                return comp
            except Exception as e:
                pass
    #downloaded xmls
    match_list = glob.glob(os.path.join(xml_dir, '*.xml')) + glob.glob(os.path.join(xml_dir, 'unable_to_process', '*.xml'))
    downloaded_match_ids = [int(i.split('.')[0].split('_')[-1]) for i in match_list]
    check_match_list = [i for i in match_id_range if i not in downloaded_match_ids]

    user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'} 
    for match_id in tqdm(check_match_list):
        if not comp:
            comp = look_for_league(match_id)
        if comp:
            url = "http://s3-irl-{}.squawka.com/dp/ingame/{}".format(comp, match_id)
            req = Request(url, headers=user_agent)
            try:
                contents = urlopen(req, timeout=10).read()
                with open(os.path.join('data', '{}_{}.xml'.format(comp, match_id)), 'wb') as f:
                    f.write(contents)
            except Exception as e:
                comp = None

if __name__ == '__main__':
    download_xmls('data', range(1, 40000))
