import http_service as http
import structure_resource
from structure_spec import Structure

class JIST:
    def __init__(self, host, username, password):
        http.init(host, username, password)

    def get_structures(self) -> list[Structure]:
        res = structure_resource.get_structures()

        return res