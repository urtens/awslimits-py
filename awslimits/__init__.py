import logging
from awslimitchecker.checker import AwsLimitChecker

logging.basicConfig()
logger = logging.getLogger()


class awsclient(object):
    def __init__(self, region):
        self.region = region
    
    def connect(self, region):
        try:
            c = AwsLimitChecker(region=region)
        except:
            print("Connection error")

        return c

    def get_thresholds(self):
        conn = self.connect(self.region)
        thresholds = conn.check_thresholds(use_ta=False)
        return thresholds

    # def get_limits(self):

