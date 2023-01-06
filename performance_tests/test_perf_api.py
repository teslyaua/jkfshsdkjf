import random

from locust import HttpUser, task, between


class ExBankUser(HttpUser):
    wait_time = between(0.5, 2.5)

    @task
    def get_user_balance(self):
        users = ['user1', 'user2']
        user_id = random.choice(users)
        self.client.get(f'/balance/{user_id}/get_balance')
