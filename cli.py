#!/usr/bin/env python

import argparse
from sys import exit
from awslimits import botoclient
import json

if __name__ == '__main__':
    client = botoclient("eu-west-1")
    print(json.dumps(client.get_current_usage()))
