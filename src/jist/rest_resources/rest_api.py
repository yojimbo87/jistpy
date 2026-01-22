from jist.rest_resources import (
    structure_resource,
    forest_resource,
    value_resource
)
from jist.specs import (
    StructureResponse,
    ForestSpec,
    ForestResponse,
    AttributeDefinition,
    ValueRequestItem,
    ValueRequest,
    ValueResponse
)


def get_structures() -> list[StructureResponse]:
    response = structure_resource.get_structures()

    return response


def get_structure(structure_id: int) -> StructureResponse:
    response = structure_resource.get_structure(structure_id)

    return response


def get_forest(structure_id: int) -> ForestResponse:
    response = forest_resource.get_forest(structure_id)

    return response


def get_value(
        structure_id: int,
        rows: list[int],
        attributes: list[AttributeDefinition]) -> ValueResponse:
    request = ValueRequest(
        requests=[
            ValueRequestItem(
                forestSpec=ForestSpec(structure_id=structure_id),
                rows=rows,
                attributes=attributes
            )
        ]
    )

    response = value_resource.get_value(request)

    return response
