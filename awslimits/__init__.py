import logging
import boto3

logging.basicConfig()
logger = logging.getLogger()

ASG_INTERESTING_KEYS = ("NumberOfLaunchConfigurations", 
        "MaxNumberOfLaunchConfigurations", 
        "MaxNumberOfAutoScalingGroups", 
        "NumberOfAutoScalingGroups")

def handle_date(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

class botoclient(object):
    def __init__(self, region):
        self.region = region
        self.ec2_limits = self.get_ec2_limits()
        self.asg_limits = self.get_asg_limits()

    def connect(self, service):
        return boto3.client(service)

    def parse_response(self, response, interesting_keys):
        return dict((k, response[k]) for k in interesting_keys if k in response)

    def get_asg_limits(self):
        """ 
        Returns a dict containing the limits and current usage
        """
        response = {}
        c = self.connect("autoscaling")
        limits = c.describe_account_limits()
        return self.parse_response(limits, ASG_INTERESTING_KEYS)

    def get_ec2_limits(self):
        """
        Queries AWS to get a dict containing the account attributes
        returns: dict
        """
        c = self.connect("ec2")
        limits = c.describe_account_attributes()
        result = {}
        for account_attribute in limits["AccountAttributes"]:
            try:
                result[account_attribute["AttributeName"]] = account_attribute["AttributeValues"][0]["AttributeValue"]
            except (IndexError, KeyError) as e:
                return None
        return result

    def get_running_ec2(self):
        c = self.connect("ec2")
        instances = c.describe_instances(Filters=[{
            "Name":"instance-state-name",
            "Values": ["running"]
            }])
        count = 0
        for reservation in instances["Reservations"]:
            count += len(reservation["Instances"])
        return count

    def get_current_usage(self):
        usage = {}
        usage["instances"] = {
                "current": self.get_running_ec2(),
                "limit": int(self.ec2_limits["max-instances"])
                }
        usage["autoscaling-groups"] = {
                "current": self.asg_limits["NumberOfAutoScalingGroups"],
                "limit": self.asg_limits["MaxNumberOfAutoScalingGroups"]
                }
        usage["launch-configurations"] = {
                "current": self.asg_limits["NumberOfLaunchConfigurations"],
                "limit": self.asg_limits["MaxNumberOfLaunchConfigurations"]
                }
        return usage

