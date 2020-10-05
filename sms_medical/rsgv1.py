#!/usr/bin/env python3

"""
The MIT License (MIT)

Copyright (c) 2016 Perfness

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

The Software is provided "as is", without warranty of any kind, express or
implied, including but not limited to the warranties of merchantability,
fitness for a particular purpose and noninfringement. In no event shall the
authors or copyright holders be liable for any claim, damages or other
liability, whether in an action of contract, tort or otherwise, arising from,
out of or in connection with the software or the use or other dealings in the
Software.
"""

import json
from http.client import HTTPConnection
from urllib.parse import urlencode


class RESTSMSGateway(object):
    def __init__(self, url, port, debug=False):
        self.conn = HTTPConnection(url, port)
        self.debug = debug

        # self._debug(str(self.conn))

    def _debug(self, *args):
        if self.debug:
            print(args)

    def _getQueryString(self, limit, offset):
        retval = ""

        if limit:
            retval += "limit=" + str(limit)
        if retval and offset:
            retval += "&"
        if offset:
            retval += "offset=" + str(offset)
        if retval:
            retval = "?" + retval

        return retval

    def getThreadAll(self, limit=None, offset=None):
        method = 'GET'
        url = '/v1/thread/%s' % self._getQueryString(limit, offset)

        self._debug(method, url)
        self.conn.request(method, url)

        resp = self.conn.getresponse()
        data = resp.read().decode("utf-8")

        if resp.status == 200:
            return json.loads(data)

        return None

    def getThreadById(self, id):
        method = 'GET'
        url = '/v1/thread/%d/' % id

        self._debug(method, url)
        self.conn.request(method, url)

        resp = self.conn.getresponse()
        data = resp.read().decode("utf-8")

        if resp.status == 200:
            return json.loads(data)

        return None

    def getSMSAll(self, limit=None, offset=None):
        method = 'GET'
        url = '/v1/sms/%s' % self._getQueryString(limit, offset)

        self._debug(method, url)
        self.conn.request(method, url)

        resp = self.conn.getresponse()
        data = resp.read().decode("utf-8")

        if resp.status == 200:
            return json.loads(data)

        return None

    def getSMSById(self, id):
        method = 'GET'
        url = '/v1/sms/%d/' % id

        self._debug(method, url)
        self.conn.request(method, url)

        resp = self.conn.getresponse()
        data = resp.read().decode("utf-8")

        if resp.status == 200:
            return json.loads(data)

        return None

    def sendSMS(self, phone, message):
        method = 'POST'
        url = '/v1/sms/?%s' % urlencode({'phone': phone, 'message': message})

        self._debug(method, url)
        self.conn.request(method, url)

        resp = self.conn.getresponse()
        data = resp.read().decode("utf-8")

        return data

    def getStatus(self):
        method = 'GET'
        url = '/v1/status/'

        self._debug(method, url)
        self.conn.request(method, url)

        resp = self.conn.getresponse()
        data = resp.read().decode("utf-8")

        if resp.status == 200:
            return json.loads(data)

        return None
