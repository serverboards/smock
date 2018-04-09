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
        response = smocked.mock_res("testjsonable")
        print("res", response)
        asjson = json.dumps(response)
        print("res as json", asjson)
        assert asjson != "{}"

    def test_file(self):
        smocked = smock.SMock("tests/data.yaml")
        res = smocked.mock_res("withfile")
        print("with file response", res)
        assert res["nofile"] == "OK"
        assert res.file.strip() == "OOK", res.file


if __name__ == '__main__':
    unittest.main()
