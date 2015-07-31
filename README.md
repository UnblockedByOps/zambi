# zambi
A single place to manage AWS boto connection objects for multiple accounts and services.

# Summary
Zambi is used to manage multiple connection types leveraging the boto library. So that you
can quickly create a new connection object for a new account or a service.

# Getting started
To get started install zambi
```
pip install zambi
```

Create a conf directory and a credential directory and set these system variables.
```
export AWS_CONF_DIR=/path/to/conf
export AWS_CRED_DIR=/path/to/credntials
```

Create account mapping file, $AWS_CONF_DIR/account_aliases_map.txt
```
opsqa:opsqa:111111111111
```

Create credential files, $AWS_CRED_DIR/opsqa.ini
```
[Credentials]
aws_account_id=111111111111
aws_access_key_id=AXXXXXXXXXXX
aws_SECRET_ACCESS_KEY=yyyyyyyxxxxxxxzzzzzz
```

# Usage
Initialize the Zambi within you.
```
from zambi import ZambiConn
cmgr = ZambiConn()
```

To get all accounts from mapping file.
```
accounts = cmgr.get_accounts()
```

To get accounts that end in qa.
```
accounts = cmgr.get_accounts('.*qa')
```

To get just the opsqa account.
```
account = cmgr.get_accounts('opsqa')
```

Creaet an EC2 Connection to opsqa.
```
conn = cmgr.get_connection(account)
```

Example of other services like route53
```
conn = cmgr.get_connection(account, service='route53')
```
