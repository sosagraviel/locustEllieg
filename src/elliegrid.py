import json
import string
import random
from locust.exception import StopUser

from locust import HttpUser, SequentialTaskSet, task, between


class WebTasks(SequentialTaskSet):
    count = 0

    def on_start(self):
        print("start")
        self.register()

    @task(1)
    def register(self):
        self.count += 1
        print(self.count)
        print("Register")
        prefix = get_random_string(4)
        verification_token = "$2a$10$SpEjDf5qlSALeNMCSKNVuO19u2eQ2SKxuUBhWxVVOIhSjNCOyy96u"
        response_register = self.client.post("/v1/register", {"name": "test",
                                                              "email": "test+" + str(prefix) + "@decemberlabs.com",
                                                              "password": "get_random_string",
                                                              "verificationToken": verification_token})
        print("this is the register response " + response_register.text + "\n")
        token_register = json.loads(response_register.text.encode('utf8'))['data']
        print("this is the token register " + token_register + "\n")

        print("validate mail")
        with self.client.get(
                "/v1/register/" + "test+" + str(prefix) + "@decemberlabs.com" + "/" + str(token_register),
                catch_response=True, name="HTTP 200") as validate_res:
            if validate_res.status_code == 200:
                print("the validate response was success " + str(validate_res.status_code) + "\n")
                validate_res.success()
            else:
                print("the validate response was failure " + str(validate_res.status_code) + "\n")
                validate_res.failure("got different status code than 200")

        print("login")
        login_res = self.client.post("/v1/authenticate", {
            "email": "test+" + str(prefix) + "@decemberlabs.com",
            "password": "get_random_string"})
        print("this is the Login response " + login_res.text + "\n")
        data_token_login = json.loads(login_res.text.encode('utf8'))['data']
        print("this is the data login " + str(data_token_login) + "\n")
        token_login = data_token_login['token']
        print("this is the token login " + str(token_login) + "\n")
        user_id_login = data_token_login['id']
        print("this is the user id login: " + str(user_id_login) + "\n")
        header = {
            'Authorization': 'Bearer ' + str(token_login),
            'content-type': 'application/json', 'accept': 'application/json'
        }
        with self.client.delete(
                "/v1/users/" + str(user_id_login), headers=header,
                catch_response=True, name="HTTP 200") as delete_user_res:
            if delete_user_res.status_code == 200:
                print("the delete response was success " + str(delete_user_res.status_code) + "\n")
                print("this is the response " + delete_user_res.text + "\n")
                delete_user_res.success()
                raise StopUser()
            else:
                print("the delete response was failure " + str(delete_user_res.status_code) + "\n")
                delete_user_res.failure("got different status code than 200 deleting the user")


class WebUser(HttpUser):
    host = "url"
    tasks = [WebTasks]
    wait_time = between(1, 9)


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
