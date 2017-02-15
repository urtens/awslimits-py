#!/usr/bin/env python

import argparse
from sys import exit
from awslimits import awsclient

if __name__ == '__main__':
    print('This is the cli')
    aws_client = awsclient()
    aws_client.get_limits()
