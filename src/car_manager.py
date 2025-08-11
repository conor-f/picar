import json
import httpx


class CarManager:
    def __init__(self, ip: str, *args, **kwargs):
        self.ip = ip
        self.base_url = f"http://{self.ip}/js?json="
        self._client = None

    async def _get_client(self):
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client

    async def perform_request(self, command: dict):
        json_command = json.dumps(command)
        print("---------------")
        print("Performing:")
        print(json_command)

        client = await self._get_client()
        response = await client.get(self.base_url + json_command)

        print("Completed. Response:")
        print(response.text)
        print("---------------")

    async def stop(self):
        command = {
            "T": 1,
            "L": 0.0,
            "R": 0.0,
        }

        await self.perform_request(command)

    async def drive(self, l_speed=0.1, r_speed=0.1):
        command = {
            "T": 1,
            "L": l_speed,
            "R": r_speed,
        }

        await self.perform_request(command)
