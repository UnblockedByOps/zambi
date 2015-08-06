import os
import zambi
import moto


def test_delete_env():
    ''' Test deleting os environmental variables. '''
    os.environ['AWS_ACCESS_KEY_ID'] = 'AWSKEYID'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'AWSSECRETKEY'
    os.environ['AWS_ACCOUNT_ID'] = '123456789012'
    assert zambi.clean_env() == True


class TestZambi(object):
    ''' testMatch class to test zambi package. '''
    def __init__(self):
        mapfile = os.getcwd() + '/tests/account_aliases_map.txt'
        self.cmgr = zambi.ZambiConn(mapfile=mapfile)

    def test_valid_mapfile(self):
        ''' Test a valid mapfile. '''
        assert self.cmgr.get_accounts('opsqa') == ['opsqa']

    def test_invalid_mapfile(self):
        ''' Test an invalid mapfile. '''
        self.cmgr = zambi.ZambiConn(mapfile='fake.txt')
        assert self.cmgr.get_accounts('opsqa') == False

    def test_multiple_accounts(self):
        ''' Test regex for multiple accounts. '''
        assert self.cmgr.get_accounts('.*prod') == [
            'biprod',
            'bzprod',
            'csprod',
            'demandprod',
            'gridprod',
            'ipprod',
            'opsprod',
            'webprod']

    def test_invalid_account(self):
        ''' Test invalid account. '''
        assert self.cmgr.get_accounts('xxxxxx') == []

    def test_invalid_conn(self):
        ''' Test invalid connections. '''
        assert self.cmgr.get_connection('xxxxx', service='s3') == False
        assert self.cmgr.get_connection('xxxxx', service='ec2') == False
        assert self.cmgr.get_connection('xxxxx', service='rds') == False
        assert self.cmgr.get_connection('xxxxx', service='rds2') == False
        assert self.cmgr.get_connection('xxxxx', service='elb') == False
        assert self.cmgr.get_connection('xxxxx', service='sqs') == False
        assert self.cmgr.get_connection('xxxxx', service='emr') == False
        assert self.cmgr.get_connection('xxxxx', service='route53') == False
        assert self.cmgr.get_connection('xxxxx', service='iam') == False

    def test_invalid_service(self):
        ''' Test an invalid service. '''
        assert self.cmgr.get_connection('opsqa', service='pizza') == False

    def test_valid_conn(self):
        ''' Test a valid connection object with moto. '''
        os.environ['AWS_CRED_DIR'] = os.getcwd() + '/tests'
        mock = moto.ec2.mock_ec2()
        mock.start()
        conn = self.cmgr.get_connection('opsqa')
        if conn:
            pass
        else:
            assert False
