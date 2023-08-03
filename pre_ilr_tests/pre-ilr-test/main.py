#####################################################
"""

Tenant Pre-Infrastructure-Live Test Cases

"""
#####################################################

import sys
import argparse

from .test_cases import *

# Method only get's called from outside after the module is created
def start_testing(args):
  results = eval(args['test_entry_point']+"()")
  return results

# This is Pip based module entry point
def main():
  arges = argparse.ArgumentParser()
  parser.add_argument("-t", "--test_type", default=None, required=False)
  parser.add_argument("-l", "--test_type", default=None, required=False)
  args = parser.parse_args(args)
  if args.test_type:
    results = eval(args.test_type+"()")

if __name__ == "__main__":
  main()
