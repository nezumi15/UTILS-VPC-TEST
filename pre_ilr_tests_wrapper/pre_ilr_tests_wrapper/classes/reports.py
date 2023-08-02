###################################################################
"""

Reports - Create Reports for the test

"""
###################################################################

import json
from datetime import datetime

class Reports:
  def __init__(self):
    pass

  def start_reporting(results):
    report = {}
    # Start Reporting
    reports['date'] = datetime.now()
    reports['results'] = results

    # Print results
    with open('pre-ilr-tests-reports-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M-%S")),'w') as fp:
      j = json.dumps(reports, sort_keys=True, indent=4, default=str)
      print(j, file=fp)

    return reports
