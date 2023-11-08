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

import xmltodict
from lxml.etree import tostring


class XMLReader():

    '''
    Converts a xml filt to a Python dictionary.
    '''
    @staticmethod
    def xml_to_dict(xml_data):

        xml_string_data  = tostring(xml_data, encoding='UTF-8', method='xml')

        data_dict = xmltodict.parse(xml_string_data)

        return data_dict

