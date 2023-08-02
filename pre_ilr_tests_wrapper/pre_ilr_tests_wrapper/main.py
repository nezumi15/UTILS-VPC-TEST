########################################################################
"""

Pre-Infrastructure-Live Test Case Wrapper

"""
########################################################################

import os
import sys
import argparse

from .classes import Questions
from .classes import Cliparser
from .classes import TestHandler
from .classes import Reports

# Change to current Working Dir
os.chdir)os.getcwd())

def main():
  args = sys.argv[1:]
  parser = argparse.ArgumentParser()
  parser.add_argument("-ui", action='store_true')
  parser.add_argument("-c", "--cli_args", nargs ='+', type=int, required=False)
  args = parser.parse_args(args)

  if args.ui:
    answers = Questions.start_inquiring()
  elif args.cli_args:
    answers = Cliparser.start_parsing(arg.cli_args)
  else:
    sys.exit(0)

  # Start running of the test
  results = TestHandler.start_testing(answers)

  # Start Reporting
  reports = Reports.start_reporting(results)

  # Test Code , remove later
  print(reports)

if __name__ == "__main__":
  main()
