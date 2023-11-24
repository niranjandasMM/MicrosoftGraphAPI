import webbrowser
import os
import msal
import ast

import environ

env = environ.Env()

APP_ID = env("APP_ID")
SCOPES = env("SCOPES")
SCOPES = ast.literal_eval(SCOPES)
GRAPH_API_ENDPOINT = env("GRAPH_API_ENDPOINT")

def generate_access_token():
    access_token_cache = msal.SerializableTokenCache()

    if os.path.exists('api_token_access.json'):
        access_token_cache.deserialize(open('api_token_access.json', 'r').read())
    
    client = msal.PublicClientApplication(client_id=APP_ID, token_cache=access_token_cache)

    accounts = client.get_accounts()

    if accounts:
        token_response = client.acquire_token_silent(SCOPES, accounts[0])
    else:  
        flow = client.initiate_device_flow(scopes=SCOPES)
        ## When the token expires or runs in a new machine, the code is required to pass during the  authentication.
        print('user code : ' + flow['user_code'])
        webbrowser.open(flow['verification_uri'])
        
        token_response = client.acquire_token_by_device_flow(flow)
    
    
    with open('api_token_access.json', 'w') as _f:
        _f.write(access_token_cache.serialize())
    return token_response

