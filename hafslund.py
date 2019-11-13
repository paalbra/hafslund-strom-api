import configparser
import copy
import re

import requests

class HafslundAPI():

    def __init__(self, config_path):
        self.config_path = config_path

        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.username = self.config["hafslund"]["username"]
        self.password = self.config["hafslund"]["password"]
        self.user_agent = self.config["hafslund"]["user_agent"]

        self.auth = self.do_auth().json()
        self.api_key = self.auth["apiKey"]
        self.token = self.auth["token"]

    def do_auth(self):
        url = "https://api.linkapp.no/user/auth-ext"
        data = {
            "username": self.username,
            "password": self.password,
            "client": "minside-web"
        }

        return self.do_request(url, data=data)

    def do_token_refresh(self):
        url = "https://api.linkapp.no/apikey/token-refresh"
        data = {
            "apiKey": self.api_key,
            "client": "minside-web"
        }

        response = self.do_request(url, data=data, auth=True)

        self.token = response.json()["token"]

        return response

    def get_consumption(self, meter_point_id, start_date, end_data, resolution):
        # resolution: hourly, week-stats
        url = f"https://api.linkapp.no/api/consumption/{meter_point_id}/{start_date}/{end_data}/{resolution}"

        return self.do_request(url, headers=headers, auth=True)

    def get_facilities(self, no_consumption=True):
        facilities = copy.deepcopy(self.auth["facilities"])
        if no_consumption:
            for facility in facilities:
                del facility["consumption"]

        return facilities

    def get_flags(self):
        url = f"https://api2.linkapp.no/api/flags"

        return self.do_request(url, auth=True)

    def do_request(self, url, data=None, headers={}, auth=False):
        headers["User-Agent"] = self.user_agent
        if auth:
            headers["Authorization"] = f"Bearer {self.token}"

        if data:
            return requests.post(url, headers=headers, json=data)
        else:
            return requests.get(url, headers=headers)
