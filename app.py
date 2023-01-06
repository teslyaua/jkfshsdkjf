from enum import Enum

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask("ExBank")
api = Api(app)
port = 5005


user_parser = reqparse.RequestParser()
user_parser.add_argument('name', required=True, type=str, help='Please provide name for new user')

balance_parser = reqparse.RequestParser()
balance_parser.add_argument('amount', required=True, type=str, help='Please provide amount')

money_parser = reqparse.RequestParser()
money_parser.add_argument('from_user_id', required=True, type=str, help='Please provide from_user_id')
money_parser.add_argument('to_user_id', required=True, type=str, help='Please provide to_user_id')
money_parser.add_argument('amount', required=True, type=str, help='Please provide amount')

users = {'user1': {'name': 'Iurii', 'balance': 10.0},
         'user2': {'name': 'Petro', 'balance': 10.0}, }


class BalanceOperations(Enum):
    deposit = 1
    withdraw = 2


def abort_if_user_doesnt_exist(user_id):
    if user_id not in users:
        abort(404, message=f"User {user_id} doesn't exist")


def abort_if_amount_negative(amount):
    if amount < 0:
        abort(400, message=f"Wrong amount:  {amount}. Amount for operation could not be negative")


def abort_if_balance_below_zero(user_id, amount):
    if users[user_id]['balance'] - amount < 0:
        abort(400, message=f"User doesn't have enough money. Current balance is {round(users[user_id]['balance'], 2)}")


def get_amount_from_args(args):
    return round(float(args['amount'].replace(',', '.')), 2)


class User(Resource):

    def get(self, user_id):
        if user_id == 'all':
            return users
        abort_if_user_doesnt_exist(user_id)
        return users[user_id]

    def put(self, user_id):
        args = user_parser.parse_args()
        new_user = {'name': args['name'], 'balance': 0}
        users[user_id] = new_user
        return {user_id: users[user_id]}

    def post(self):
        args = user_parser.parse_args()
        next_id = int(max(users.keys()).lstrip('user')) + 1
        user_id = f'user{next_id}'
        users[user_id] = {'name': args['name'], 'balance': 0}
        return {user_id: users[user_id]}, 201

    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        del users[user_id]
        return ''


class Balance(Resource):

    def get(self, user_id: str):
        if user_id == 'all':
            return users
        abort_if_user_doesnt_exist(user_id)
        return users[user_id]['balance']

    def put(self, user_id: str, operation: str):
        args = balance_parser.parse_args()
        amount = get_amount_from_args(args)
        abort_if_user_doesnt_exist(user_id)
        abort_if_amount_negative(amount)
        if operation == BalanceOperations.withdraw.name:
            abort_if_balance_below_zero(user_id, amount)
            users[user_id]['balance'] -= amount
        elif operation == BalanceOperations.deposit.name:
            users[user_id]['balance'] += amount
        else:
            abort(400, message=f"Only withdraw and deposit methods have been implemented")
        return users[user_id]


class Money(Resource):

    def post(self):
        args = money_parser.parse_args()
        amount = get_amount_from_args(args)
        abort_if_balance_below_zero(args['from_user_id'], amount)

        users[args['from_user_id']]['balance'] -= amount
        users[args['to_user_id']]['balance'] += amount
        return [users[args['from_user_id']], users[args['to_user_id']]]


api.add_resource(User, '/users/<user_id>', '/users/create_user')
api.add_resource(Balance, '/balance/<user_id>/get_balance', '/balance/<user_id>/<operation>')
api.add_resource(Money, '/money/send')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
