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

from webex_xml_api import XMLAPI, SendRequestError
from workflow import ConfigurationWorkflow
import os

from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":

    site_name = os.environ['SITENAME']
    webex_id = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    audio_pin = os.environ['AUDIO_PIN']
    host_pin = os.environ['HOST_PIN']
    
    try:   
        xml_api = XMLAPI(site_name, webex_id, password, None, audio_pin, host_pin)
    
    except SendRequestError as err:
        print(err)
        raise SystemExit

    ConfigurationWorkflow.audio_conference_configuration(xml_api, site_name)