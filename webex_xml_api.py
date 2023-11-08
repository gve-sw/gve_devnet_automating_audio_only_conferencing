"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests
from lxml import etree

# Change to true to enable request/response debug output
DEBUG = False

# Custom exception for errors when sending requests
class SendRequestError(Exception):

    def __init__(self, result, reason):
        self.result = result
        self.reason = reason

    pass


class XMLAPI():

    def __init__(self, siteName, webExId, password, accessToken, audio_pin, host_pin):
        self.siteName = siteName
        self.webExId = webExId
        self.audio_pin = audio_pin
        self.host_pin = host_pin
        self.sessionTicket = self.AuthenticateUser(password, accessToken)


    def AuthenticateUser(self, password, accessToken):
        # If an access token is provided via the oauth workflow, we'll use this form
        if ( accessToken != None ):
            request = f'''<?xml version="1.0" encoding="UTF-8"?>
            <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <securityContext>
                        <siteName>{self.siteName}</siteName>
                        <webExID>{self.webExId}</webExID>
                    </securityContext>
                </header>
                <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.AuthenticateUser">
                        <accessToken>{accessToken}</accessToken>
                    </bodyContent>
                </body>
            </serv:message>'''
        else:
            # If no access token, assume a password was provided, using this form
            request = f'''<?xml version="1.0" encoding="UTF-8"?>
                <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <header>
                        <securityContext>
                            <webExID>{self.webExId}</webExID>
                            <password>{password}</password>
                            <siteName>{self.siteName}</siteName>
                        </securityContext>
                    </header>
                    <body>
                        <bodyContent xsi:type="java:com.webex.service.binding.user.AuthenticateUser"/>
                    </body>
                </serv:message>'''

        response = self.sendRequest(request)

        #print(etree.tostring( response, pretty_print = True, encoding = 'unicode' ))

        #print(response.find( '{*}body/{*}bodyContent/{*}sessionTicket' ).text)

        # Return the sessionTicket
        return response.find( '{*}body/{*}bodyContent/{*}sessionTicket' ).text


    def SetUserInfo(self, first_name, last_name, email):
        
        request = f'''<?xml version="1.0" encoding="UTF-8"?>
            <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <securityContext>
                        <siteName>{self.siteName}</siteName>
                        <webExID>{self.webExId}</webExID>
                        <sessionTicket>{self.sessionTicket}</sessionTicket>
                    </securityContext>
                </header>
                <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.SetUser">
                        <webExId>{email}</webExId>
                        <use:firstName>{first_name}</use:firstName>
                        <use:lastName>{last_name}</use:lastName>
                        <use:phones>                
                        <PIN>{self.audio_pin}</PIN>
                        </use:phones>

                        <personalMeetingRoom>
                            <hostPIN>{self.host_pin}</hostPIN>
                        </personalMeetingRoom>


                    </bodyContent>
                </body>
            </serv:message>'''

        response = self.sendRequest( request )

        return response


    def GetUser(self,email):

        request = f'''<?xml version="1.0" encoding="UTF-8"?>
            <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <securityContext>
                        <siteName>{self.siteName}</siteName>
                        <webExID>{self.webExId}</webExID>
                        <sessionTicket>{self.sessionTicket}</sessionTicket>
                    </securityContext>
                </header>
                <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.GetUser">
                        <webExId>{email}</webExId>
                    </bodyContent>
                </body>
            </serv:message>'''

        response = self.sendRequest( request )

        #print(etree.tostring( response, pretty_print = True, encoding = 'unicode' ))

        return response


    def SetCallInfo(self, email):

        request = f'''<?xml version="1.0" encoding="UTF-8"?>
            <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <securityContext>
                        <siteName>{self.siteName}</siteName>
                        <webExID>{self.webExId}</webExID>
                        <sessionTicket>{self.sessionTicket}</sessionTicket>
                    </securityContext>
                </header>
                <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.SetUser">
                        <webExId>{email}</webExId>
                        <personalTeleconf>
                            <account>
                                <accountIndex>1</accountIndex>
                                <autoGenerate>true</autoGenerate>
                                <defaultFlag>true</defaultFlag>
                                <joinBeforeHost>false</joinBeforeHost>
                            </account>
                        </personalTeleconf>
                    </bodyContent>
                </body>
            </serv:message>'''

        response = self.sendRequest( request )

        #print(etree.tostring( response, pretty_print = True, encoding = 'unicode' ))

        return response
    
    # Generic function for sending XML API requests
    # envelope : the full XML content of the request
    def sendRequest(self, envelope):

        #if DEBUG:
        #    print( envelope )

        # Use the requests library to POST the XML envelope to the Webex API endpoint
        response = requests.post( 'https://api.webex.com/WBXService/XMLService', envelope )

        # Check for HTTP errors
        try: 
            response.raise_for_status()
        except requests.exceptions.HTTPError as err: 
            raise SendRequestError( 'HTTP ' + str(response.status_code), response.content.decode("utf-8") )

        # Use the lxml ElementTree object to parse the response XML
        message = etree.fromstring( response.content )

        if DEBUG:
            print( etree.tostring( message, pretty_print = True, encoding = 'unicode' ) )   

        # Use the find() method with an XPath to get the 'result' element's text
        # Note: {*} is pre-pended to each element name - ignores namespaces
        # If not SUCCESS...
        if message.find( '{*}header/{*}response/{*}result').text != 'SUCCESS':

            result = message.find( '{*}header/{*}response/{*}result').text
            reason = message.find( '{*}header/{*}response/{*}reason').text

            #...raise an exception containing the result and reason element content
            raise SendRequestError( result, reason )

        return message


