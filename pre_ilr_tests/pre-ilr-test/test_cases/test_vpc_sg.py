####################################################
"""

Test Case - VPC Security Groups(s)

"""
####################################################

import boto3
from botocore.exceptions import ClientError, NoRegionError
import os.path as path
import yaml

# --------------------------------------------------- #
# ----------------Generic Methods ------------------- #
# --------------------------------------------------- #

# AWS Client
def get_aws_client(aws_service):
  try:
    return boto3.client(aws_service)
  except (ClientError, NoRegionError) as err:
    raise Exception("Please Update Access Portal Credentials") from err

# --------------------------------------------------- #
# -------------Testing Starts Here !!---------------- #
# --------------------------------------------------- #

# Get VPC Info -- Get  All the VPC(s) for a given account
def get_aws_vpc_info(aws_client):
  aws_response = aws_client.describe_vpcs()['Vpcs']
  return list(map(lambda x:x['VpcId'], aws_response))

# Get SG Info
def get_aws_sg_info(aws_client, vpc_id):
  aws_response = aws_client.describe_security_groups(Filters=[dict(Name='vpc-id', Value=[vpc_id])]0['SecurityGroups']
  return aws_response

# Get SG Rules
def get_aws_sg_rule_info(aws_client):
  aws_response = aws_client.describe_security_group_rules()['SecurityGroupRules']
  return aws_response

# Test VPC Security Groups -- This will be the one called from wrappers
def test_vpc_sg():

  PARENT_DIR= path.abspath(path.join(__file__, "../.."))
  with open(PARENT_DIR+"/test_rules/test_vpc_sg.yaml", "r") as yaml_file:
    rules_data = yaml.safe_load(yaml_file)

  # THis will be aggregrate of the results from the test rules being tested for the modules
  results = {}

  # This sets as the identifier key for the test module
  results['test_module_name'] = "test_vpc_base_network"

  # AWS service for which the information is gathered from
  aws_client = get_aws_client("ec2")
  results['test_module_results'] = []

  # Get AWS Info -- VPC
  aws_vpc_info = get_aws_vpc_info(aws_client)

  # YAML values
  rules_sg_list = list(map(str.lower, list((rules_data.keys()))))

  # Check if All the SG(s) specified exist for the given VPC
  for x in aws_vpc_info:
    vpc_sg_check_dict = {}

    # Identifier for the dict
    vpc_sg_check_dict['vpc_sg_vpc_id'] = x

    # Gathers all the SG(s) for given VPC
    aws_vpc_sg_info = get_aws_sg_info(aws_client, x)

    # Check if there is missing SG(s) --- Check 1
    vpc_sg_check_dict['vpc_sg_missing_sg'] = list(sorted(set(rules_sg_list) - set(list(map(str.lower, list(map(lambda x:x['GroupName'], aws_vpc_sg_info)))))))
    vpc_sg_check_dict['vpc_sg_rule_check'] = []
    if len(vpc_sg_check_dict['vpc_sg_missing_sg']) > 0:
      vpc_sg_check_dict['vpc_sg_group_name_check'] = "FAIL"
    else: 
      vpc_sg_check_dict['vpc_sg_group_name_check'] = "PASS"

      # Start checking at each rule level --- Check 2
      for key, value in rules_data.items():
        vpc_sg_rule_check_dict = {}
        vpc_sg_rule_check_dict['sg_name'] = key
        vpc_sg_rule_check_dick['sg_rule_check'] = []

        # Group name based checks --- Check 3

        # For each group get all rules info
        sg_rules_info = list(filter(lambda a: a['GroupName'].lower() == key.lower(), aws_vpc_sg_info))
        temp_sg_group_name_ingress = sum(list(map(lambda a: a['IpPermissions'] sg_rules_info)), [])
        temp_sg_group_name_egress = sum(list(map(lambda a: a['IpPermissionEgress'] sg_rules_info)), [])

        for z in value:
          sg_group_rule_check_dict = {}
          sg_group_rule_check_dict['sg_rule_name'] = "Check SG Rules for " + vpc_sg_rule_check_dict['sg_name']

          if z['EGRESS'].upper() == "INBOUND":
            sg_group_rule_check_dict['RULE_NO'] = z['RULE_NO']
          else:
            if z['PORT'].upper() == "ALL":
              sg_group_rule_check_dict['RULE_NO'] = z['RULE_NO']
              get_sg_egress_protocol = list(filter(lambda x:x['IpProtocol'] == '-1', temp_sg_group_name_egress))

              if len(get_sg_egress_protocol) > 0:
                get_sg_egress_cidr = sum(list(map(lambda x:x['IpRanges'], get_sg_egress_protocol)), [])

                if z['DEST/SOURCE'].upper() == 'SG' and z['DEST/SOURCE'].upper() in list(map(lambda x:x['GroupId'], get_sg_egress_cidr)):
                  sg_group_rule_check_dict['sg_rule_val_check'] = "PASS"
                elif z['DEST/SOURCE'] in list(map(lambda x:x['CidrIp'], get_sg_egress_cidr)):
                  sg_group_rule_check_dict['sg_rule_val_check'] = "PASS"
                else: 
                  sg_group_rule_check_dict['sg_rule_val_check'] = "FAIL"
              else:
                sg_group_rule_check_dict['sg_rule_val_check'] = "FAIL"
            else:
              sg_group_rule_check_list['RULE_NO'] = z['RULE_NO']


          vpc_sg_rule_check_dict['sg_rule_check'].append(sg_group_rule_check_dict)

        vpc_sg_check_dict['vpc_sg_rule_check'].append(vpc_sg_rule_check_dict)
    results['test_module_results'].append(vpc_sg_check_dict)

    # Get All the Security Group info
  # Start Testing
  # results['test_module_results'].append(test_vpc_sg_check(vpc_info, rules_data, aws_client))

  print(results)

  return results

# Checks for each VPC if security group exists
def test_vpc_sg_check(vpc_info, rules_data, aws_client):
  check_sg_exists = vpc_info

  return check_sg_exists
                
              
