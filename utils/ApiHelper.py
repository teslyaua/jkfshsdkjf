import json
import os

import allure
from requests import request

from utils.ApiResponse import ApiResponse
from utils.general_utils import prettify_dict, logger


class ApiHelper:
    USER_ENDPOINT = '/users'
    BALANCE_ENDPOINT = '/balance'
    MONEY_ENDPOINT = '/money'

    def __init__(self):
        self._base_url = f'{os.environ.get("HOST")}:{os.environ.get("PORT")}'
        self._headers = {'accept': 'application/json', "Content-Type": 'application/json'}
        self.status_code = 0

    @allure.step
    def create_user(self, user):
        logger.info(f'POST Body create new user: \n {prettify_dict(user)}')
        response = request('post', f'{self._base_url}{self.USER_ENDPOINT}/create_user',
                           headers=self._headers,
                           data=json.dumps(user))

        return ApiResponse(response)

    @allure.step
    def get_all_users(self):
        response = request('get', f'{self._base_url}{self.USER_ENDPOINT}/all',
                           headers=self._headers)

        return ApiResponse(response)

    @allure.step
    def get_users_by_id(self, user_id):
        response = request('get', f'{self._base_url}{self.USER_ENDPOINT}/{user_id}',
                           headers=self._headers)

        return ApiResponse(response)

    @allure.step
    def delete_user(self, user_id):
        response = request('delete', f'{self._base_url}{self.USER_ENDPOINT}/{user_id}',
                           headers=self._headers)

        return ApiResponse(response)

    @allure.step
    def get_all_users(self):
        response = request('get', f'{self._base_url}{self.USER_ENDPOINT}/all',
                           headers=self._headers)

        return ApiResponse(response)

    @allure.step
    def deposit(self, user_id, data):
        logger.info(f'PUT Deposit Body: \n {prettify_dict(data)}')
        response = request('put', f'{self._base_url}{self.BALANCE_ENDPOINT}/{user_id}/deposit',
                           headers=self._headers,
                           data=json.dumps(data))

        return ApiResponse(response)

    @allure.step
    def withdraw(self, user_id, data):
        logger.info(f'PUT Withdraw Body: \n {prettify_dict(data)}')
        response = request('put', f'{self._base_url}{self.BALANCE_ENDPOINT}/{user_id}/withdraw',
                           headers=self._headers,
                           data=json.dumps(data))

        return ApiResponse(response)

    @allure.step
    def send_money(self, data):
        logger.info(f'POST Send Money Body: \n {prettify_dict(data)}')
        response = request('post', f'{self._base_url}{self.MONEY_ENDPOINT}/send',
                           headers=self._headers,
                           data=json.dumps(data))

        return ApiResponse(response)
