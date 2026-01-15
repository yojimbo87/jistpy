import http_service as http
import rest_resources as rest_resources
from specs import Structure

class JIST:
    def __init__(self, host, username, password):
        http.init(host, username, password)

    def get_structures(self) -> list[Structure]:
        response = rest_resources.get_structures()

        return response
    
    def get_structure(self, structure_id: int) -> Structure:
        response = rest_resources.get_structure(structure_id)

        return response