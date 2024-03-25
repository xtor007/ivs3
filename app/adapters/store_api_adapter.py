import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway

from config import (
    STORE_API_UPLOAD_URL
)


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        try:
            data = []
            for model in processed_agent_data_batch:
                data.append(model.json())
            json_data = "[" + ",".join(data) + "]"

            res = requests.post(
                STORE_API_UPLOAD_URL,
                data=json_data
            )
            res.raise_for_status()
            return (res.status_code > 199) and (res.status_code < 300)
        except requests.RequestException as error:
            print(error)
            return False
