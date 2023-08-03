#####################################################
"""

Test Case - VPC Base Network
- Test VPC CIDR
- Test VPC NGW
- Test VPC S3 Endpoint
- Test VPC TGW
- Test VPC VPG

"""
######################################################

import boto3
from botocore.exceptions import ClientError, NoRegionError

# -------------------------------------------------- #
# -------------- Generic Methods ------------------- #
# -------------------------------------------------- #

# AWS Client
def get_aws_client(aws_service):
  try:
    return boto3.client(aws_service)
  except (ClientError, NoRegionError) as err:
    raise Exception("Please Update Access Portal Crentials") from err

# -------------------------------------------------- #
# ----------- Testing Starts Here !!---------------- #
# -------------------------------------------------- #
# test VPC Base Network -- This will be the one called from wrappers
def test_vpc_base_network():

  # This will be aggregate of the results from the test rules being tested for the modules
  results = {}

  # This sets as the identifier key for the test module
  results['test_module_name'] = "test_vpc_base_network"

  # AWS Service for which the information is gathered from
  aws_client = get_aws_client("ec2")
  results['test_module_results'] = []
  results['test_module_results'].append(test_vpc_cidr(aws_client))
  results['test_module_results'].append(test_vpc_ngw(aws_client))
  results['test_module_results'].append(test_vpc_s3_endpoints(aws_client))
  results['test_module_results'].append(test_vpc_tgw(aws_client))
  results['test_module_results'].append(test_vpc_vpg(aws_client))
  return results
