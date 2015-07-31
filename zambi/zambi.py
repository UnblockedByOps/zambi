# Copyright 2015 CityGrid Media, LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
''' Zambi is a connection manager that creates connnection objects
to manage multiple AWS accounts and services. '''

import os
import re
import sys
import boto
from boto import s3
from boto import rds
from boto import ec2
from boto import sqs
from boto import emr
from boto import iam
from boto import rds2
from boto import route53
from boto.ec2 import elb


class ZambiConn(object):
    ''' Zambi Connection manager manages connections to multiple AWS accounts
    and services. '''
    def __init__(self):
        self.conn = None
        self.conf = None
        self.mapfile = '%s/%s' % (os.getenv('AWS_CONF_DIR'),
                                  'account_aliases_map.txt')

    def get_accounts(self, pattern='.*'):
        ''' Get a list of accounts based on a regex. Default
        is to get all accounts.'''
        accounts = list()
        try:
            mfile = open(self.mapfile)
        except IOError, msg:
            print >> sys.stderr, 'ERROR: %s' % msg
            return False
        for line in mfile.readlines():
            if not re.match('^#', line):
                account = line.split(':')[1]
                if re.match(pattern, account):
                    if account not in accounts:
                        accounts.append(account)
        return accounts

    def get_connection(self, acct_name, service='ec2', region='us-east-1'):
        ''' Returns a connection object to AWS. Defaults,
        service=ec2, region=us-east-1 '''
        if os.getenv('AWS_ACCESS_KEY_ID'):
            print >> sys.stderr, (
                'WARN: Zambi does not work with shell-environment ',
                'AWS credentials, deleting environment ',
                'variables and continuing')
            del os.environ['AWS_ACCESS_KEY_ID']
            del os.environ['AWS_SECRET_ACCESS_KEY']
            del os.environ['AWS_ACCOUNT_ID']
        self.conf = '%s/%s/%s.ini' % (os.getenv('AWS_CRED_DIR'),
                                      acct_name, acct_name)
        try:
            boto.config.load_credential_file(self.conf)
        except IOError, msg:
            print >> sys.stderr, 'ERROR: %s' % msg
            return False
        if service == 's3':
            self.conn = s3.connect_to_region(region)
        if service == 'ec2':
            self.conn = ec2.connect_to_region(region)
        if service == 'rds':
            self.conn = rds.connect_to_region(region)
        if service == 'rds2':
            self.conn = rds2.connect_to_region(region)
        if service == 'elb':
            self.conn = elb.connect_to_region(region)
        if service == 'sqs':
            self.conn = sqs.connect_to_region(region)
        if service == 'emr':
            self.conn = emr.connect_to_region(region)
        if service == 'route53':
            self.conn = route53.connect_to_region(region)
        if service == 'iam':
            self.conn = iam.connect_to_region('universal')
        if not self.conn:
            print >> sys.stderr, 'ERROR: Unknown service'
            return False
        return self.conn
