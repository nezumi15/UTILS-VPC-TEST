###################################################################
"""

Questions - For the User Questions and Answers inputs 

"""
###################################################################

import inquirer
import sys
from inquirer import errors
from ..constants.common_constants import (
  TEST_MSG,
  PRE_ILR_QUESTIONS,
  QUESTIONS_THEME,
  CMN_TEST_EXIT,
  CMN_TEST_RUN_ALL
)

class Questions:
  def __init__(self):
    pass

  def start_inquiring():

    # Determine what set of questions to Ask based on Tag
    questions = [
      inquirer.List(
        "test_option", message=TEST_MSG, choices=list(map(lambda x: x['test_msg'], PRE_ILR_QUESTIONS))
      ),
    ]

    # Prompt Users for the Question
    answers = inquirer.prompt(
      questions, theme=inquirer.themes.load_theme_from_dict(QUESTIONS_THEME)
    )

    if answers['test_option'] == CMN_TEST_EXIT:
      sys.exit(0)
    elif answers['test_option'] == CMN_TEST_RUN_ALL:
      answers = PRE_ILR_QUESTIONS
    else:
      answers = list(filter(lambda x: x['test_msg'] == answers['test_option'], PRE_ILR_QUESTIONS))

    return answers
