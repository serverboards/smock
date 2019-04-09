#!/usr/bin/python3

import smock
import json
import unittest


class SMockTest(unittest.TestCase):
    def test_basic_smock(self):
        import requests
        smocked = smock.SMock("tests/data2.yaml", "tests/data.yaml")
        requests.get = smocked.mock_method("requests.get")
        res = requests.get("https://mocked.url")
        print(res)

        assert res.status_code == 200, res
        assert res.content == "Gocha!", res
        assert res.json() == {"text": "Gocha too!"}, res.json()
        assert int(res.status_code) == 200, type(res.status_code)
        assert float(res.status_code) == 200.0, type(res.status_code)
        assert str(res.status_code) == "200", type(res.status_code)

        res = requests.get("https://mocked.data2.url")
        assert res.status_code == 200, res

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

    def test_ops(self):
        a = smock.wrapped(100)
        b = smock.wrapped(200)

        assert a < 200
        assert b > 100
        assert a < b
        assert b > a

        assert a <= 100
        assert b >= 200
        assert a >= 100
        assert b <= 200
        assert a <= b
        assert b >= a

        assert a != b
        assert a == a

    def test_hashable(self):
        a = smock.wrapped(10)

        assert a not in [20, 30]
        assert a in [10, 20, 30]
        assert 10 in [a, 20, 30]
        assert hash(a) == hash(10)

    def test_ops(self):
        a = smock.wrapped(0.0)
        b = smock.wrapped(10.0)
        c = smock.wrapped(3.0)

        assert (a or 1.0) == 1.0
        assert (a and 1.0) == 0.0
        assert (b or 1.0) == 10.0
        assert (b and 1.0) == 1.0

        assert (0 or a) == 0.0
        assert (a and 1.0) == 0.0
        assert (b or 1.0) == 10.0
        assert (b and 1.0) == 1.0

        assert (a * 10) == 0.0
        assert (b * 10) == 100.0
        assert (b * c) == 30.0

        assert (a / 10) == 0.0
        assert (b / 10) == 1.0
        assert (b / 10.0) == 1.0
        assert (b / c) > 3.333 and (b / c) < 3.334

        assert (a // 10) == 0
        assert (b // 10) == 1
        assert (b // 10.0) == 1
        assert (b // c) == 3

        assert -b == -10.0

        assert not smock.wrapped(False), True

        assert (smock.wrapped(True) ^ smock.wrapped(True)) is False


if __name__ == '__main__':
    unittest.main()
