#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import httplib2
from google.appengine.api import memcache
import os

from googleapiclient.discovery import build

from oauth2client.client import GoogleCredentials

# The project id whose datasets you'd like to list
from oauth2client.contrib.gce import AppAssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials

PROJECTID = 'bq-devfest-demo-2016'

scopes = ['https://www.googleapis.com/auth/bigquery']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.path.join(os.path.dirname(__file__), 'devfest.json'), scopes)

http_auth = credentials.authorize(httplib2.Http())
service = build('bigquery', 'v2', http=http_auth)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        createDataSet(self)


def createDataSet(self):
    dataset = service.datasets()
    data = buildDataSetBody()
    dataset.insert(projectId=PROJECTID, body=data).execute()
    self.response.write(dataset)


def buildDataSetBody():
    fields = {}
    fields['projectId'] = "bq-devfest-demo-2016"
    fields['datasetId'] = "DevFestClient"
    obj = {}
    obj['datasetReference'] = fields

    return obj


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
