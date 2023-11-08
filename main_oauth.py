# Copyright (c) 2023 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

from flask import Flask, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
import json
import os
from webex_xml_api import XMLAPI, SendRequestError
from workflow import ConfigurationWorkflow

from dotenv import load_dotenv
load_dotenv()

# Change to true to enable request/response debug output
DEBUG = False

# Instantiate the Flask application
app = Flask(__name__)

# This key is used to encrypt the Flask user session data store,
# you might want to make this more secret
app.secret_key = "CHANGEME"

# Create an Authlib registry object to handle OAuth2 authentication
oauth = OAuth(app)

# This simple function returns the authentication token object stored in the Flask
# user session data store
# It is used by the webex RemoteApp object below to retrieve the access token when
# making API requests on the session user's behalf
def fetch_token():

    return session[ 'token' ]

# Webex returns no 'token_type' in its /authorize response.
# This authlib compliance fix adds its as 'bearer'
def webex_compliance_fix( session ):

    def _fix( resp ):

        token = resp.json()

        token[ 'token_type' ] = 'bearer'

        resp._content = json.dumps( token ).encode( 'utf-8' )

        return resp

    session.register_compliance_hook('access_token_response', _fix)

# Register a RemoteApplication for the Webex Meetings XML API and OAuth2 service
# The code_challenge_method will cause it to use the PKCE mechanism with SHA256
# The client_kwargs sets the requested Webex Meetings integration scope
# and the token_endpoint_auth_method to use when exchanging the auth code for the
# access token
oauth.register(

    name = 'webex',
    client_id = os.environ['CLIENT_ID'],
    client_secret = os.environ['CLIENT_SECRET'],
    authorize_url = 'https://webexapis.com/v1/authorize',
    access_token_url = 'https://webexapis.com/v1/access_token',
    refresh_token_url = 'https://webexapis.com/v1/authorize',
    api_base_url = 'https://api.webex.com/WBXService/XMLService',
    client_kwargs = { 
        'scope': 'spark-admin:telephony_config_read spark-admin:telephony_config_write spark:all spark-admin:telephony_config_read spark:telephony_config_write meeting:admin_config_read meeting:admin_config_write',
        'token_endpoint_auth_method': 'client_secret_post' 
    },
    code_challenge_method = 'S256',
    fetch_token = fetch_token,
    compliance_fix=webex_compliance_fix
)

# The Flask web app routes start below
# This is the entry point of the app - navigate to https://localhost:5000 to start
@app.route('/')
def login():

    # Create the URL pointing to the web app's /authorize endpoint
    redirect_uri = url_for( 'authorize', _external=True)

    print(redirect_uri)
    # Use the URL as the destination to receive the auth code, and
    # kick-off the Authclient OAuth2 login flow
    return oauth.webex.authorize_redirect( redirect_uri )


# This URL handles receiving the auth code after the OAuth2 flow is complete
@app.route('/authorize')
def authorize():

    # Go ahead and exchange the auth code for the access token
    # and store it in the Flask user session object
    try:
        session['token'] = oauth.webex.authorize_access_token()

    except Exception as err:

        print(err)

        response = 'Error exchanging auth code for access token:<br>'
        response += '<ul><li>Error: ' + err + '</li>'

        return response, 500        

    # Now that we have the API access token, redirect the the URL for making a
    # Webex Meetings API GetUser request

    return redirect( url_for( 'AudioConferenceConfig' ), code = '302' )


@app.route('/AudioConferenceConfig')
def AudioConferenceConfig():

    site_name = os.environ['SITENAME']
    webex_id = os.environ['USERNAME']
    audio_pin = os.environ['AUDIO_PIN']
    host_pin = os.environ['HOST_PIN']
    token = session['token']['access_token']
    
    try:   
        xml_api = XMLAPI(site_name, webex_id, None, token, audio_pin, host_pin)
    
    except SendRequestError as err:
        return f"{err.result}: {err.reason}", 500

    ConfigurationWorkflow.audio_conference_configuration(xml_api, site_name)

    response = "Process complete" 
        
    return response


if __name__ == "__main__":
    app.run(debug=True)