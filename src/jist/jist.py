import utils.http_service as http
import rest_resources as rest_resources
from specs import (
    StructureResponse, 
    ForestSpec, 
    Forest, 
    AttributeDefinition, 
    ValueRequestItem, 
    ValueRequest, 
    ValueResponse
)

class JIST:
    def __init__(self, host, username, password):
        http.init(host, username, password)

    def get_structures(self) -> list[StructureResponse]:
        response = rest_resources.get_structures()

        return response
    
    def get_structure(self, structure_id: int) -> StructureResponse:
        response = rest_resources.get_structure(structure_id)

        return response
    
    def get_forest(self, structure_id: int) -> Forest:
        response = rest_resources.get_forest(structure_id)

        return response
    
    def get_value(self, structure_id: int, rows: list[int], attributes: list[AttributeDefinition]) -> ValueResponse:
        request = ValueRequest(
            requests=[
                ValueRequestItem(
                    forestSpec=ForestSpec(structure_id=structure_id),
                    rows=rows,
                    attributes=attributes
                )
            ]
        )
        
        response = rest_resources.get_value(request)

        return response