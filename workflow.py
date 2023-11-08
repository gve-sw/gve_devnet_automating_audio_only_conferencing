
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

from csv_reader import CSVReader
from xml_reader import XMLReader
from mailing_service import Mail
from webex_xml_api import SendRequestError
import os

from dotenv import load_dotenv
load_dotenv()


class ConfigurationWorkflow():

    @staticmethod
    def audio_conference_configuration(xml_api, site_name):

        # Read users from csv file
        users = CSVReader.csv_to_dict(os.environ['USER_CSV_FILENAME'])

        #For each user in the csv file
        for index in range(len(users['First Name'])):

            first_name = users['First Name'][index]
            last_name = users['Last Name'][index]
            email = users['Email'][index]

            print(f"---Starting process for {email}")

            try:
                #Set User Info
                response = xml_api.SetUserInfo( 
                    first_name, 
                    last_name, 
                    email
                    )

            except SendRequestError as err:
                print("Error while setting user info:")
                print(err)
                raise SystemExit

            try:
                #Set Call Info
                response = xml_api.SetCallInfo( 
                    email
                    )

            except SendRequestError as err:
                print("Error while setting call info:")
                print(err)
                raise SystemExit

            try:
                #Read User Info
                user_data_xml = xml_api.GetUser( 
                    email
                    )

            except SendRequestError as err:
                print("Error while getting User info:")
                print(err)
                raise SystemExit

            #Convert audio config info xml to json format
            user_data_json = XMLReader.xml_to_dict(user_data_xml)

            #Retrieve relevant data from returned user data
            receiver_email = user_data_json['serv:message']['serv:body']['serv:bodyContent']['use:email'] 
            host_access_code = user_data_json['serv:message']['serv:body']['serv:bodyContent']['use:personalTeleconf']['use:account']['use:subscriberAccessCode']
            host_pin_code = user_data_json['serv:message']['serv:body']['serv:bodyContent']['use:phones']['use:hostPIN']
            attendee_access_code = user_data_json['serv:message']['serv:body']['serv:bodyContent']['use:personalTeleconf']['use:account']['use:participantFullAccessCode']
            audio_pin_code = user_data_json['serv:message']['serv:body']['serv:bodyContent']['use:phones']['use:PIN']

            #Send email based on html template to each user
            mail_service = Mail(os.environ['EMAIL_SENDER'], os.environ['EMAIL_APP_PASSWORD'])
            mail_service.send_mail(receiver_email, host_access_code, attendee_access_code, host_pin_code, audio_pin_code, site_name, attachment=False)

