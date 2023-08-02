#########################################################################
"""

Pre ILR Test Wrapper Common Constants values for the util

"""
#########################################################################
import os

# Custom Theme for the cookie cutter
QUESTIONS_THEME = {
  "Question": {
    "mark_color": "yellow",
    "brackets_color": "normal",
    "default_color": "white",
  },
  "List": {
    "selection_color": "bold_red",
    "selection_cursor": "=>",
    "unselected_color": "bold_blue",
  },
}

# AWS BOTO3 Constants
CONST_EC2 = "ec2"
AWS_ERR_MSG = "Please Update C2S Access Portal Credentials"

# Test Msg
TEST_MSG = "Please Select the Type of Test"

# Questions
CMN_TEST_EXIT = "Exit"
CMN_TEST_RUN_ALL = "Test All"

PRE_ILR_QUESTIONS = [
  {
    "test_num" : 0,
    "test_msg" : CMN_TEST_EXIT,
    "test_entry_point" : "NONE"
  },
  {
    "test_num" : 1,
    "test_msg" : CMN_TEST_EXIT,
    "test_entry_point" : "NONE"
  },
  {
    "test_num" : 2,
    "test_msg" : CMN_TEST_EXIT,
    "test_entry_point" : "NONE"
  },
  {
    "test_num" : 3,
    "test_msg" : CMN_TEST_EXIT,
    "test_entry_point" : "NONE"
  }
]
