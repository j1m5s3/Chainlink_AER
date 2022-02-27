import unittest
import random
import string
import requests
import json
from app import APP

class MyTestCase(unittest.TestCase):

    def test_get_weather_by_city_info(self):
        weather_by_city_req_obj = {'data': {'city_name': 'Boston', 'field': 'temp'}}
        tester = APP.test_client(self)
        response = tester.post('/', json=weather_by_city_req_obj)
        result = json.loads(response.data)
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)

        pass


def local_test_suite(testcase_class):
    suite = unittest.TestSuite()
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(testcase_class)
    suite.addTest(tests)
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_results = runner.run(local_test_suite(MyTestCase))
    print("--------------------------")
    print(len(test_results.failures))
    pass