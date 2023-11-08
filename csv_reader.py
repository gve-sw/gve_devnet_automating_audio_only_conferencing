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

import pandas as pd

class CSVReader():

    '''
    Converts a csv filt to a Python dictionary.
    '''
    @staticmethod
    def csv_to_dict(filename):
        
        data_dict = pd.read_csv(f'{filename}').to_dict()
        
        return data_dict


    '''
    Converts a csv filt to a json file.
    '''
    @staticmethod
    def csv_to_json_file(filename):

        data = pd.read_csv(f'{filename}')
        data.to_json(path_or_buf=f'{filename}.json',orient='records')


