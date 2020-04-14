import os
import sys
import glob
import shutil
import pandas as pd
from tqdm import tqdm

sys.path.append('squawka-scraper')
from squawka.utils import SquawkaReport

def remove_xmls(xml_dir):
    """
    Remove xmls that can't be processed to a sub folder: unable_to_process.
    
    Parameters
    ----------
    xml_dir, str, path to xml folder.
    """
        
    # define a subfolder to save xmls that can't be processed
    fail_xml_dir = os.path.join(xml_dir, 'unable_to_process')
    
    xml_paths = glob.glob(os.path.join(xml_dir, '*.xml'))
    fail_xml_paths = []

    for xml in tqdm(xml_paths):
        try:
            report = SquawkaReport(xml)
            stats = pd.DataFrame(getattr(report, 'teams'))
            stats['kickoff'] = report.kickoff
            # use pass data to check event data integrity
            pass_df = pd.DataFrame(getattr(report, 'all_passes'))
            if pass_df.shape[0] == 0: #no event data
                fail_xml_paths.append(xml)
            elif len(pass_df.mins.unique()) < 60: # incomplete event data
                fail_xml_paths.append(xml)
        except Exception as e:
            fail_xml_paths.append(xml)
        
    if len(fail_xml_paths) != 0:
        for xml in fail_xml_paths:
            shutil.move(xml, os.path.join(fail_xml_dir, xml.split('\\')[-1]))

if __name__ == '__main__':
    remove_xmls('data')