from setuptools import setup, find_packages
from pathlib import Path

setup(
  name="pre-ilr-tests",
  version="0.0.1",
  install_requires=[
    "boto3==1.24.9",
    "botocore==1.27.37",
    "argparse==1.4.0",
    "pydantic==2.1.1",
    "pydantic_core==2.4.0"
  ],
  packages=find_packages(),
  entry_points={
    "console_scripts": [
      "pre_ilr_tests = pre_ilr_tests.main:main",
    ]
  },
  include_package_data=True,
  package_data={
    'pre_ilr_tests.test_rules':['*.yaml']
  }
)
