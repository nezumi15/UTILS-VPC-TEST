####################################################################
"""

Questions - for the User Questions and Answers inputs

"""
####################################################################

import sys
from ..constants.common_constants import (
  TEST_MSG,
  PRE_ILR_QUESTIONS,
  QUESTIONS_THEME,
  CMN_TEST_EXIT,
  CMN_TEST_RUN_ALL
)

class Cliparser:
  def __init__(self):
    pass

  def start_parsing(cli_args):
    answers =[]
    for x in cli_args:
      if x == 0:
        sys.exit(0)
      elif x == 1:
        answers = PRE_ILR_QUESTIONS
        break
      else:
        answers.append(list(filter(lambda y: y['test_num'] == x, PRE_ILR_QUESTIONS))[0])
    return answers
