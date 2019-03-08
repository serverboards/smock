#!/usr/bin/python3

import smock
import json
import unittest


class SMockTest(unittest.TestCase):
    def test_basic_smock(self):
        import requests
        smocked = smock.SMock("tests/data.yaml")
        requests.get = smocked.mock_method("requests.get")
        res = requests.get("https://mocked.url")
        print(res)

        assert res.status_code == 200, res
        assert res.content == "Gocha!", res
        assert res.json() == {"text": "Gocha too!"}, res.json()
        assert int(res.status_code) == 200, type(res.status_code)
        assert float(res.status_code) == 200.0, type(res.status_code)
        assert str(res.status_code) == "200", type(res.status_code)

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

    def test_attr_get(self):
        smocked = smock.SMock("tests/data.yaml")
        res = smocked.mock_res("withfile")
        try:
            a = res.notexists
            raise Exception("Should raise!")
        except AttributeError:
            pass
        except:
            raise Exception("Should raise AttributeError!")
        try:
            a = res["notexists"]
            raise Exception("Should raise!")
        except KeyError:
            pass
        except:
            raise Exception("Should raise AttributeError!")


if __name__ == '__main__':
    unittest.main()
