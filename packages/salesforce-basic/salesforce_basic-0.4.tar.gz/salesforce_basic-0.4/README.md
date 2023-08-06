# salesforce_basic

Simple Python API client library for Salesforce

## Installation

To install run `pip install salesforce_basic`.

## Running

This is a simple wrapper to the salesforce REST API (https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_rest_resources.htm) which includes oauth authentication.

To use:

```python
from salesforce_basic import SalesforceBasicConnector

connector = SalesforceBasicConnector(sandbox = False, **kwargs)
```

The kwargs to create the connector set up the url to talk to and the oauth related tokens.  The oauth tokens can either by read from an AWS ssm parameter (if 'region_name' and 'name' keywords are passed) or passed directly via the keywords 'client_id', 'client_secret', 'access_token' 'refresh_token' and 'request_url'.

The library uses version 44.0 of the rest API

To make requests and get json back do:

```
response = connector.do_request(locator, data = None, patch = False)
```

Where locator is the restful API (the class prefixes it with '/services/data/v44.0').
If data is passed then a POST request is made (unless patch is passed, in which case a PATCH request is made).

The connector class gets a new oauth access_token if the access_token has expired and refresh_token is still active.











