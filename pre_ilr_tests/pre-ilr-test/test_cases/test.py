import boto3
import yaml
from termcolor import colored

# Read config.yaml file
with open("config.yaml", "r") as stream:
  configdict = yaml.safe_load(stream)

# boto3 calls for account SG data
client = boto3.client('ec2')
response_sg = client.security_groups()['SecurityGroups']
response_sgr = client.describe_security_group_rules()['SecurityGroupRules']
response_cidr = client.describe_vpcs()['Vpcs'][0]['CidrBlockAssociationSet']

# Fail multi-VPC environments pleasantly
try:
  multi_vpc_test = client.describe_vpcs()['Vpcs'][1]['CidrBlockAssociationSet']
except:

  # Handle 'default' group-name capitalization differences
  try: 
    response_default_sg = client.describe_security_groups(Filers=[{'Name':'group-name', 'Values':['default'],},],)['SecurityGroups']
  except:
    response_default_sg = client.describe_security_groups(Filers=[{'Name':'group-name', 'Values':['DEFAULT'],},],)['SecurityGroups']
  else:
    response_default_sg = client.describe_security_groups(Filers=[{'Name':'group-name', 'Values':['default'],},],)['SecurityGroups']

  def retrieve_sgs():
    sg_list_account = []
    for sg in response_sg:
      sg_list_account.append(sg['GroupName'])
    return sg_list_account

  def retrieve_sg_ids():
    sg_list_id_account = []
    for sg in response_sg:
      if sg['GroupName'].upper() in configdict:
        sg_list_id_account.append(sg['GroupId'])
    return sg_list_id_account

  # Define variables
  sgs_in_account_unf = retrieve_sgs()
  expected_sg_list = []
  sgs_in_account = [x.upper() for x in sgs_in_account_unf]
  total_expected_sg = 0
  for sg in configdict : total_expected_sg += 1
  sg_ids_in_account = []
  sg_ids_in_account = retrieve_sg_ids()
  account_expected_rules_list = []
  account_rules_list = []
  account_rule_counts = []
  account_expected_rules_list_common = []
  from_port = ""
  ip_protocol = ""
  destsrc = ""

  def compare_expected_sgs_to_account ():
    for sg in configdict:
      if sg in sgs_in_account:
        print(colored("PASS", "green") + (": ") + sg + " SG exists within the account")
      else:
        print(colored("FAIL", "red") + (": ") + sg + " SG DOES NOT exist within the account")

  def count_account_sg_rules(account_expected_rules_list):
    # Count rules in Account's SG
    acccount_rule_counts = [0]*total_expected_sg
    y=0
    for expected_sg in configdict:
      for sg_rule in account_expected_rules_list:
        if sg_rule.startswith(str(expected_sg)):
          account_rule_counts[y] = account_rule_counts[y] + 1
      y+=1
    return account_rule_counts

  def create_sort_all_expected_rules_list():
    # Create, sort all rules for account SGs that are in the expected SG list
    for sg_rule in response_sgr:
      if sg_rule['GroupId'] in sg_ids_in_account:
        for sg in response_sg:
          if sg_rule['GroupId'] == sg['GroupId']:
            group_name = sg['GroupName'].upper()
            break
        if sg_rule['IsEgress']:
          egress = 'OUTBOUND'
        else:
          egress = 'INBOUND'
        if sg_rule['IpProtocol'] == "-1":
          ip_protocol = "ALL"
        else:
          ip_protocol = sg_rule['IpProtocol'].upper()
        if sg_rule['FromPort'] == -1:
          from_port = "ALL"
        elif sg_rule['FromPort'] == 3:
          from_port = "DEST UNR"
        else:
          from_port = str(sg_rule['FromPort'])
        # Sees if a CIDR is in rule and records it if present, if no CIDR it checks for prefixlist and record prefixlist if present, otherwise assumes 'self' SG rule
        try:
          sg_rule['CidrIpv4']
        except KeyError:
          try:
            sg_rule['PrefixListId']
          except KeyError:
            # Assumes rule is the 'self' sg rule if no CIDR or prefix list is present
            account_expected_rules_list.append(group_name + "|" + egress + "|" + ip_protocol + "|" + from_port + "|" + sg_rule['GroupId'] + sg_rule['GroupId'].upper() + "/" + sg_rule['SecurityGroupRuleId'].upper())
          else:
            account_expected_rules_list.append(group_name + "|" + egress + "|" + ip_protocol + "|" + from_port + "|" + sg_rule['PrefixListId'] + sg_rule['GroupId'].upper() + "/" + sg_rule['SecurityGroupRuleid'].upper())
        else:
          account_expected_rules_list.append(group_name + "|" + egress + "|" + ip_protocol + "|" + from_port + "|" + sg_rule['CidrIpv4'] + sg_rule['GroupId'].upper() + "/" + sg_rule['SecurityGroupRuleid'].upper())
      account_expected_rules_list.sort()
      return account_expected_rules_list

    def create_sort_all_rules_list():
      # Create, sort all rules for account SGs that are in the expected SG list
      for sg_rule in response_sgr:
        for sg in response_sg:
          if sg_rule['GroupId'] == sg['GroupId']:
            group_name = sg['GroupName'].upper()
            break
        if sg_rule['IsEgress']:
          egress = 'OUTBOUND'
        else:
          egress = 'INBOUND'
        if sg_rule['IpProtocol'] == "-1":
          ip_protocol = "ALL"
        else:
          ip_protocol = sg_rule['IpProtocol'].upper()
        if sg_rule['FromPort'] == -1:
          from_port = "ALL"
        elif sg_rule['FromPort'] == 3:
          from_port = "DEST UNR"
        else:
          from_port = str(sg_rule['FromPort'])
        # Sees if a CIDR is in rule and records it if present, if no CIDR it cheks for prefixlist and records prefixlist if present, otherwise assumes 'self' SG rule
        try:
          sg_rule['CidrIpv4']
        except KeyError:
          try:
            sg_rule['PrefixListId']
          except KeyError:
            # Assumes rule is the 'self' sg rule if no CIDR or prefix list is present
            account_rules_list.append(group_name + "|" + egress + "|" + ip_protocol + "|" + from_port + "|" + sg_rule['GroupId'] + sg_rule['GroupId'].upper() + "/" + sg_rule['SecurityGroupRuleId'].upper())
          else:
            account_rules_list.append(group_name + "|" + egress + "|" + ip_protocol + "|" + from_port + "|" + sg_rule['PrefixListId'] + sg_rule['GroupId'].upper() + "/" + sg_rule['SecurityGroupRuleId'].upper())
        else:
          account_rules_list.append(group_name + "|" + egress + "|" + ip_protocol + "|" + from_port + "|" + sg_rule['CidrIpv4'] + sg_rule['GroupId'].upper() + "/" + sg_rule['SecurityGroupRuleId'].upper())
      account_rules_list.sort()
      return account_rules_list

    def calculate_expected_rule_counts():
      c=0
      y=0
      expected_rule_counts=[0]*total_expected_sg
      for sg in configdict:
        for rule in configdict[sg]:
          y+=1
        expected_rule_counts[c]=y
        y=0
        c+=1
      return expected_rule_counts

    def compare_rule_counts():
      account_expected_rules_list = create_sort_all_expected_rules_list()
      account_rules_list = create_sort_all_rules_list()
      # Count rules in Account's SG
      accound_rule_counts = count_account_sg_rules(account_expected_rules_list)
      # Compare expected rules per SG to account's rules per SG
      z=0
      rule_count_comparison = []
      expected_rules_count = []
      expected_rules_counts = calculate_expected_rule_counts()
      for expected_rule_count in expected_rules_counts:
        if expected_rule_count == account_rule_counts[z]:
          rule_count_comparison.append("PASS")
        else:
          rule_count_comparison.append("WARNING")
        z+=1
      comparison_map = dict(zip(configdict, rule_count_comparison))
      k=0

      for key in comparison_map:
        if comparison_map[key] == "PASS":
          print(colored(comparison_map[key], "green") + ": The amount of " + key + " rules equals " + str(account_rule_counts[k]) + " when " + str(expected_rules_counts[k]) + " are expected")
        else:
          print(compariso_map[key] + ": The amount of " + key + " rules equals " + str(account_rule_counts[k]) + " when " + str(expected_rules_counts[k]) + " are expected")
          k+=1

      def print_all_rules(account_rules_list):
        text = input (colored("COMPARISON COMPLETE", "green") + " - Do you also want to print all rules that are within the account? [only 'y' prints rules]")
        if test == "y":

          print(colored("Account SG rules:", "magenta"))
          account_rules_list_split = [x.split("|") for x in account_rules_list]
          sg_tracker = ""
          for x in account_rules_list_split:
            if sg_tracker == x[0]:
              print(x[1]+"|"+x[2]+"|"+x[3]+"|"+colored(x[4], "magenta")+"|"+x[5])
            else:
              print(" ")
              print(x[0])
              print(x[1]+"|"+x[2]+"|"+x[3]+"|"+colored(x[4], "magenta")+"|"+x[5])
            sg_tracker = x[0]
          print(" ")

        def compare_individual_rules():

          # Removes unique values such as SG IDs and SG rule IDs from account rules list
          account_expected_rules_list_split = [x.split("|") for x in account_expected_rules_list]
          for x in account_expected_rules_list_split:
            account_expected_rules_list_common.append(str(x[0]+"|"+x[1]+"|"+x[2]+"|"x[3]+"|"+x[4]))
          for exp_sg in configdict:
            print(exp_sg)
            for exp_rule in configdict[exp_sg]:
              hit = False
              for acc_rule in account_expected_rules_list_common:
                if exp_rule['DEST/SOURCE'] == 'PUBLICCIDR':
                  destsrc = response_cidr[0]['CidrBlock']
                elif exp_rule['DEST/SOURCE'] == 'PRIVATECIDR':
                  destsrc = response_cidr[1]['CidrBlock']
                elif exp_rule['DEST/SOURCE'] == 'SG':
                  destsrc = exp_rule['DEST/SOURCE']
                exp_rule_in_format = exp_sg + "|" + exp_rule['EGRESS'] + "|" + exp_rule['PROTOCOL'] + "|" + exp_rule['PORT'] + "|" + destsrc
                if acc_rule.startswith(exp_rule_in_format):
                  hit = True
                if hit:
                  print(colored("PASS", "green") + (": ") + "Expected rule " + exp_rule['EGRESS'] + "|" + exp_rule['PROTOCOL'] + "|" + exp_rule['PORT'] "|" + colored(destsrc, "magenta") + " is in the account")
                else:
                  print(colored("FAIL", "red") + (": ") + "Expected rule " + exp_rule['EGRESS'] + "|" + exp_rule['PROTOCOL'] + "|" + exp_rule['PORT'] "|" + colored(destsrc, "magenta") + " is NOT in the account")
              print("  ")

            # Run the script
            compare_expected_sgs_to_account()
            compare_rule_counts()
            compare_individual_rules()
            print_all_rules(account_rules_list)

        # Finish exception for multi-vpc failing
        else:
          print(colored("This test only supports single VPC environments and this account has multiple VPCs. Stay tuned for multiple VPC support in a future test version.", "red"))
          
                                      
