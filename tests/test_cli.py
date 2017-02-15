import unittest
from httmock import with_httmock

class TestCli(unittest.TestCase):

    def test_ec2_instance_limit(self):
        self.assertEquals(200, 300) 
