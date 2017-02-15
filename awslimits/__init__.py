from awslimitchecker.checker import AwsLimitChecker
from pprint import pprint


class awsclient(object):
    def __init__(self):
        self.region = "eu-west-1"
        
    def get_limits(self):
        client = AwsLimitChecker(region=self.region)
        thresholds = client.check_thresholds()
        pprint(thresholds)
