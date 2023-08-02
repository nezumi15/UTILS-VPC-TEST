############################################################
"""

Test Handler - Decides on which test will be run

"""
###########################################################

import pre_ilr_tests
from yaspin import yaspin
from ..constants.common_constants import (
  CMN_TEST_EXIT,
  CMN_TEST_RUN_ALL
)

class TestHandler:
  def __init__(self):
    pass

  @yaspin(test="Running the Tests").white.bold.shark.on_blue
  def start_testing(answers):
    result = []

    for x in answers:
      if x['test_msg'] == CMN_TEST_EXIT or x['test_msg'] == CMN_TEST_RUN_ALL :
        continue
      else:
        results.append(pre_ilr_tests.start_testing(x))
    return results
