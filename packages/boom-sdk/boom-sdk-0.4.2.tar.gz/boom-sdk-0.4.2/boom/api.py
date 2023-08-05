import json
import os

import requests
import six

from boom import encoder


class API(object):
    urls = {
        "index": "/",
        "account": "/account/{client}",
        "authenticate": "/account/authenticate",
        "client": "/client/{client}",
        "client-location": "/client/{client}/location/{location}",
        "client-location-experience": "/client/{client}/location/{location}/experience/{experience}",
        "client-location-platform": "/client/{client}/location/{location}/platform/{platform}",
        "conversation": "/conversation/{conversation}",
        "conversation-link": "/conversation/{conversation}/link/{code}",
        "experience": "/experience/{experience}",
        "message": "/message/{message}",
        "payment": "/order/{order}/payment/{payment}",
        "payment-credentials": "/client/{client}/location/{location}/credentials",
        "payment-method": "/payment/method/{payment_method}",
        "platform": "/platform/{platform}",
        "order": "/order/{order}",
        "order-payment": "/order/{order}/payment/{payment}",
        "order-payment-method": "/order/{order}/payment/method/{method}",
        "order-search": "/order/search",
        "order-status-update": "/order/status/{status}",
        "receipt-send": "/order/{order}/payment/{payment}/receipt",
        "refund": "/order/{order}/payment/{payment}/refund/{refund}",
        "wallet": "/payment/wallet/{identifier}/consume",
        "wallet-adjust": "/payment/wallet/{identifier}/adjust"
    }

    def __init__(self, authorization=None):
        self.api_url = self.url = os.getenv("BOOM_API_URL", "https://api.boom.app")
        self.authorization = authorization

    def get_headers(self):
        headers = {
            "Content-Type": "application/json"
        }

        if self.authorization:
            headers["Authorization"] = self.authorization

        return headers

    def make_url(self, path, querystring=None):
        if path.startswith("/"):
            path = path[1:]

        if querystring:
            querystring = "?{0}".format(six.moves.urllib.parse.urlencode(querystring))
        else:
            querystring = ""

        return "{0}/{1}{2}".format(self.url, path, querystring)

    def generate_endpoint_url(self, endpoint, data=None, **kwargs):
        # Normalize the URL
        path = self.urls.get(endpoint, "")
        if path.startswith("/"):
            path = path[1:]

        querystring = {}
        data = data or {}

        # Replace all tokens in the API URL with the values from data
        for key, value in six.iteritems(kwargs):
            path, updated = self.update_path(path, key, value)
            if not updated and value:
                querystring[key] = value

        for key, value in six.iteritems(data):
            path, updated = self.update_path(path, key, value)

        # If the path ends with a token, that means we are probably creating
        # and don't have a specific item we are working with. Remove the trailing token.
        if path.endswith("}"):
            path = path[0:path.rfind("/")]

        url = self.make_url(path, querystring)
        return url

    @staticmethod
    def update_path(path, key, value):
        # Wrap the key in {}, like client => {client}
        updated = False
        if key.endswith("_id"):
            key = key[:-3]
        token = "{" + key + "}"
        if token in path:
            updated = True
            path = path.replace(token, value)

        return path, updated

    @staticmethod
    def normalize_data(data):
        if isinstance(data, dict):
            data = [data]

        return data

    @staticmethod
    def encode_data(data):
        data = json.dumps(data, cls=encoder.BoomJSONEncoder)
        return data

    def get(self, endpoint, **kwargs):
        url = self.generate_endpoint_url(endpoint, **kwargs)
        headers = self.get_headers()
        dataset = requests.get(url, headers=headers)
        dataset = dataset.json()
        dataset = self.normalize_data(dataset)

        return dataset

    def post(self, endpoint, data, **kwargs):
        headers = self.get_headers()
        data = self.encode_data(data)
        url = self.generate_endpoint_url(endpoint, **kwargs)
        dataset = requests.post(url, headers=headers, data=data)
        dataset = dataset.json()

        return dataset

    def patch(self, endpoint, data, **kwargs):
        headers = self.get_headers()
        data = self.encode_data(data)
        url = self.generate_endpoint_url(endpoint, **kwargs)
        dataset = requests.patch(url, headers=headers, data=data)
        dataset = dataset.json()

        return dataset

    def delete(self, endpoint, data, **kwargs):
        headers = self.get_headers()
        data = self.encode_data(data)
        url = self.generate_endpoint_url(endpoint, **kwargs)
        requests.delete(url, headers=headers, data=data)

        return True
