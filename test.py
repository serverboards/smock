#!/usr/bin/python3

import smock
import sys
import json
import unittest


class SMockTest(unittest.TestCase):
    def test_docs(self):
        import doctest
        res = doctest.testmod(smock, report=True, verbose=True)
        assert not res.failed

    def test_json(self):
        smocked = smock.SMock("tests/data.yaml")
        response = smocked.mock_res("requests.get", "https://mocked.url")
        print(response)
        asjson = json.dumps(response)
        assert asjson != "{}"
        print(asjson)


if __name__ == '__main__':
    unittest.main()
