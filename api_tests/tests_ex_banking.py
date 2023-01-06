import random
from http import HTTPStatus

import allure
import pytest as pytest

from fixtures.error_messages import USER_ERROR_MESSAGE, BALANCE_NEGATIVE_AMOUNT_ERROR_MESSAGE, BALANCE_BELOW_ZERO_ERROR_MESSAGE
from utils.ApiHelper import ApiHelper
from utils.general_utils import pattern, fake, today, validate_json, load_json, logger

api_helper = ApiHelper()


@allure.feature('[API] Create User')
@allure.title("[POST] Create valid user")
@allure.description("""
POSITIVE
Create valid user
""")
@pytest.mark.api
@pytest.mark.smoke
def test_create_valid_user():
    logger.info('STEP_1 : Create test data')
    new_user_body = {"name": f'{pattern}_{fake.word()}_{today()}'}

    logger.info('STEP_2 : Create new user and check status code')
    created_user_resp = api_helper\
        .create_user(new_user_body)\
        .status_code_is(HTTPStatus.CREATED)\
        .get_response_body()

    logger.info('STEP_3 : Validate result')
    user_id = list(created_user_resp.keys())[0]
    assert created_user_resp[user_id]['name'] == new_user_body['name']

    is_schema_valid = validate_json(created_user_resp[user_id], load_json('fixtures/UserSchema.json'))
    assert is_schema_valid is True, 'schema for user is not valid'


@allure.feature('[API] Create User')
@allure.title("[POST] Create invalid user")
@allure.description("""
NEGATIVE
Create invalid user
""")
@pytest.mark.api
@pytest.mark.regression
def test_create_invalid_user():
    logger.info('STEP_1 : Create test data')
    new_user_body = None

    logger.info('STEP_2 : Create new user and check status code')
    created_user_resp = api_helper\
        .create_user(new_user_body)\
        .status_code_is(HTTPStatus.BAD_REQUEST)\
        .get_response_body()

    logger.info('STEP_3 : Validate error message')
    assert USER_ERROR_MESSAGE in str(created_user_resp['message']), 'Error message is not correct'


@allure.feature('[API] Balance')
@allure.title("[PUT] Deposit")
@allure.description("""
POSITIVE
Deposit positive amount for user
""")
@pytest.mark.api
@pytest.mark.smoke
def test_deposit_positive_amount(new_user):
    logger.info('STEP_1 : Create test data with new user')
    new_user_id = new_user
    amount = round(random.uniform(0.33, 100.66), 2)

    logger.info('STEP_2 : Deposit positive amount for user')
    deposit_resp = api_helper\
        .deposit(new_user_id, data={'amount': amount})\
        .status_code_is(HTTPStatus.OK)\
        .get_response_body()

    is_schema_valid = validate_json(deposit_resp, load_json('fixtures/BalanceSchema.json'))
    assert is_schema_valid is True, 'schema for balance is not valid'

    logger.info('STEP_3 : Get user details')
    user_resp = api_helper\
        .get_users_by_id(new_user_id)\
        .status_code_is(HTTPStatus.OK)\
        .get_response_body()

    logger.info('STEP_4 : Validate user balance')
    assert user_resp['balance'] == amount, 'User balance is not correct'


@allure.feature('[API] Balance')
@allure.title("[PUT] Withdraw")
@allure.description("""
POSITIVE
Withdraw money less than user have on his balance account
""")
@pytest.mark.api
@pytest.mark.smoke
def test_withdraw_less_than_balance(new_user_with_money):
    logger.info('STEP_1 : Create test data for existing user')
    user_id = new_user_with_money
    amount = round(random.uniform(0.33, 9.66), 2)

    logger.info('STEP_2 : Withdraw positive amount for user')
    withdraw_resp = api_helper\
        .withdraw(user_id, data={'amount': amount})\
        .status_code_is(HTTPStatus.OK)\
        .get_response_body()

    is_schema_valid = validate_json(withdraw_resp, load_json('fixtures/BalanceSchema.json'))
    assert is_schema_valid is True, 'schema for balance is not valid'

    logger.info('STEP_3 : Get user details')
    user_resp = api_helper\
        .get_users_by_id(user_id)\
        .status_code_is(HTTPStatus.OK)\
        .get_response_body()

    logger.info('STEP_4 : Validate user balance')
    assert user_resp['balance'] == 10 - amount, 'User balance is not correct'


@allure.feature('[API] Balance')
@allure.title("[PUT] Deposit / Withdraw negative amount")
@allure.description("""
NEGATIVE
Deposit / Withdraw negative amount
""")
@pytest.mark.api
@pytest.mark.regression
def test_deposit_withdraw_negative_amount(new_user):
    logger.info('STEP_1 : Create test data for new user')
    new_user_id = new_user
    amount = round(random.uniform(-10.33, -0.66), 2)

    logger.info('STEP_2 : Deposit positive amount for user')
    deposit_resp = api_helper\
        .deposit(new_user_id, data={'amount': amount})\
        .status_code_is(HTTPStatus.BAD_REQUEST)\
        .get_response_body()

    logger.info('STEP_3 : Withdraw positive amount for user')
    withdraw_resp = api_helper\
        .withdraw(new_user_id, data={'amount': amount})\
        .status_code_is(HTTPStatus.BAD_REQUEST)\
        .get_response_body()

    logger.info('STEP_4 : Validate error message')
    assert BALANCE_NEGATIVE_AMOUNT_ERROR_MESSAGE in str(deposit_resp['message']), 'Error message is not correct'
    assert BALANCE_NEGATIVE_AMOUNT_ERROR_MESSAGE in str(withdraw_resp['message']), 'Error message is not correct'


@allure.feature('[API] Money')
@allure.title("[PUT] Send correct amount of money between 2 users")
@allure.description("""
POSITIVE
Send correct amount of money between 2 users
""")
@pytest.mark.api
@pytest.mark.smoke
def test_send_correct_amount_money(new_user, new_user_with_money):
    logger.info('STEP_1 : Create test data for existing users')
    from_user_id = new_user_with_money
    to_user_id = new_user
    amount = round(random.uniform(0.33, 9.66), 2)

    logger.info('STEP_2 : Send money to new user')
    send_money_resp = api_helper\
        .send_money(data={'from_user_id': from_user_id,
                          'to_user_id': to_user_id,
                          'amount': amount,
                          })\
        .status_code_is(HTTPStatus.OK)\
        .get_response_body()

    is_schema_valid = validate_json(send_money_resp, load_json('fixtures/MoneySchema.json'))
    assert is_schema_valid is True, 'schema for balance is not valid'

    logger.info('STEP_3 : Get users details')
    from_user_resp = api_helper\
        .get_users_by_id(from_user_id)\
        .get_response_body()

    to_user_resp = api_helper\
        .get_users_by_id(to_user_id)\
        .get_response_body()

    logger.info('STEP_4 : Validate users balances')
    assert from_user_resp['balance'] == 10 - amount, 'From User balance is not correct'
    assert to_user_resp['balance'] == amount, 'To User balance is not correct'


@allure.feature('[API] Money')
@allure.title("[PUT] Send more money, than user have")
@allure.description("""
NEGATIVE
Send more money, than user have in balance account
""")
@pytest.mark.api
@pytest.mark.smoke
def test_send_more_money_than_user_have(new_user, new_user_with_money):
    logger.info('STEP_1 : Create test data for existing users')
    from_user_id = new_user_with_money
    to_user_id = new_user
    amount = round(random.uniform(10.33, 19.66), 2)

    logger.info('STEP_2 : Send money to new user')
    send_money_resp = api_helper\
        .send_money(data={'from_user_id': from_user_id,
                          'to_user_id': to_user_id,
                          'amount': amount,
                          })\
        .status_code_is(HTTPStatus.BAD_REQUEST)\
        .get_response_body()

    logger.info('STEP_4 : Validate error message')
    assert BALANCE_BELOW_ZERO_ERROR_MESSAGE in str(send_money_resp['message']), 'Error message is not correct'

