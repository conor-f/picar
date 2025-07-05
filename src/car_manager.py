import json
import requests


class CarManager:
    def __init__(self, ip: str, *args, **kwargs):
        self.ip = ip
        self.base_url = f"http://{self.ip}/js?json="

    def perform_request(self, command: dict):
        json_command = json.dumps(command)
        print("---------------")
        print("Performing:")
        print(json_command)

        response = requests.get(self.base_url + json_command)

        print("Completed. Response:")
        print(response.text)
        print("---------------")

    def stop(self):
        command = {
            "T": 1,
            "L": 0.0,
            "R": 0.0,
        }

        self.perform_request(command)

    def drive(self, l_speed=0.1, r_speed=0.1):
        command = {
            "T": 1,
            "L": l_speed,
            "R": r_speed,
        }

        self.perform_request(command)
