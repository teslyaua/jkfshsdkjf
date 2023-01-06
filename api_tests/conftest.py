import pytest

from utils.ApiHelper import ApiHelper
from utils.general_utils import pattern, fake, today, logger

api_helper = ApiHelper()


@pytest.fixture(scope="function")
def new_user():
    logger.info('Setup  - Create new user')
    new_user_body = {"name": f'{pattern}_{fake.word()}_{today()}'}
    created_user_resp = api_helper.create_user(new_user_body).get_response_body()
    user_id = list(created_user_resp.keys())[0]
    yield user_id
    logger.info('Tear Down - Delete user')
    api_helper.delete_user(user_id)


@pytest.fixture(scope="function")
def new_user_with_money():
    logger.info('Setup  - Create new user and add money to account')
    new_user_body = {"name": f'{pattern}_{fake.word()}_{today()}'}
    created_user_resp = api_helper.create_user(new_user_body).get_response_body()
    user_id = list(created_user_resp.keys())[0]
    api_helper.deposit(user_id, data={'amount': 10})
    yield user_id
    logger.info('Tear Down - Delete user')
    api_helper.delete_user(user_id)
