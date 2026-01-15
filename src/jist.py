import http_service as http
import rest_resources as rest_resources
from structure_spec import Structure

class JIST:
    def __init__(self, host, username, password):
        http.init(host, username, password)

    def get_structures(self) -> list[Structure]:
        res = rest_resources.get_structures()

        return res