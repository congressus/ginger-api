"""
Created on Sept 9, 2014

Copyright 2014 Congressus, The Netherlands

Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

__title__ = 'Ginger API Wrapper'
__version__ = '1.0.0'
__author__ = 'Sjoerd Huisman'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2014 Congressus, The Netherlands'

import requests
import sys

from endpoints import *
from exceptions import *


class GingerAPI:
    WRAPPER_VERSION = '1.0'
    API_ENDPOINT = 'https://api.gingerpayments.com'
    API_VERSION = 'v1'

    def __init__(self, api_key=None):
        # requests.packages.urllib3.add_stderr_logger()
        # set API variables
        self.api_endpoint = self.API_ENDPOINT.strip().rstrip('/')
        self.api_version = self.API_VERSION.strip()
        self.version_strings = []
        self.version_strings.append('Python/' + sys.version.split(' ')[0])
        self.version_strings.append('Ginger/' + self.WRAPPER_VERSION)

        # API key
        if api_key is None:
            raise GingerAPIError('Please provide an API key')
        self.api_key = api_key

        # endpoints
        self.merchants = Merchants(self)
        self.orders = Orders(self)
        self.ideal_issuers = IdealIssuers(self)
        self.partners = Partners(self)

    def call_api(self, request_method, path, request_data=None, request_params=None):

        # make request
        request_url = '/'.join([self.api_endpoint, self.api_version, path]) + '/'
        request_headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'User-Agent': ' '.join(self.version_strings)
                }
        request_auth = (self.api_key, '')

        response = requests.request(request_method, request_url,
                                    headers=request_headers,
                                    auth=request_auth,
                                    params=request_params,
                                    data=request_data
                                    )
        # print response.content

        # decode response to JSON
        try:
            result = response.json()
        except Exception as e:
            raise GingerAPIError('Unable to decode API response from expected JSON to Dict')

        # detect API return errors
        if 'error' in result:
            raise HTTPError(result, response.request)

        return result
