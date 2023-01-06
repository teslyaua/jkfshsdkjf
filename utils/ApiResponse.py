import allure
from curlify2 import curlify
from requests import Response
from requests_toolbelt.utils import dump

from utils.general_utils import logger


class ApiResponse:

    def __init__(self, response: Response):
        self.headers = response.headers
        self._request = response.request
        self._status_code = response.status_code
        self._url = response.url
        self._response = response
        logging(response)

    def status_code_is(self, expected_status_code: int):
        """
        Asserts status code of the response.
        :param expected_status_code:
        :return:
        """
        assert self._status_code == expected_status_code, f'The status code should be: {expected_status_code}'
        return self

    def get_response_body(self):
        return self._response.json()


def logging(response):
    logger.debug(dump.dump_all(response).decode('utf-8', errors='ignore'))
    allure.attach(dump.dump_all(response).decode('utf-8', errors='ignore'), 'ROUNDTRIP-LOG')
    allure.attach((curlify.to_curl(response.request)), 'REQUEST-CURL')
    return response
