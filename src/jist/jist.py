import utils.http_service as http
from rest_resources import rest_api


class JIST:
    def __init__(self, host, username, password):
        http.init(host, username, password)

        self.rest_api: rest_api
