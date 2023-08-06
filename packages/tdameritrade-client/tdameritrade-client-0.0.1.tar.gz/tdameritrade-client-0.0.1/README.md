# TDAmeritrade Client

A tool that links to the TDA API to perform requests.

## Installation:
1. Run `pip install tdameritrade-client` within a virtual environment

## Usage
The package has two uses as of now:
1. Run the oauth flow against a developer app.
2. Use an access token to request account positions.

To get started, use the following code snippet:

``` python
from tdameritrade-client import TDClient

td_client = TDClient(acct_number=<your account number>,
                     oauth_user_id=<the id registered to the TD app you would like to authenticate with>,
                     redirect_uri=<the redirect URI registered to the TD app>,
                     token_path=<optional path to an existing access token>)
td_client.run_auth()
acct_info = td_client.get_positions()
```
