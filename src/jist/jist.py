import jist.utils.http_service as http
from jist.specs import (
    AttributeSpec,
    Structure,
    StructureRow
)
from jist.rest_resources import rest_api


class JIST:
    def __init__(self, host: str, username: str, password: str):
        http.init(host, username, password)

        self.rest_api: rest_api = rest_api

    # Loads structure data with default view attributes
    def load_structure_view(self, structure_id: int) -> Structure:
        view_response = self.rest_api.get_default_view(structure_id)

        attribute_specs: list[AttributeSpec] = []

        for column_spec in view_response.spec.columns:
            attribute_id: str = ""
            attribute_format = "text"
            attribute_params: dict = {}

            if column_spec.key == "field":
                attribute_id = column_spec.params["field"]
            elif column_spec.key == "formula":
                attribute_id = "expr"
                attribute_params = column_spec.params

            attribute_specs.append(
                AttributeSpec(
                    id=attribute_id,
                    format=attribute_format,
                    params=attribute_params
                )
            )

        return self.load_structure_attributes(structure_id, attribute_specs)

    # Loads structure data for specified attributes
    def load_structure_attributes(
            self, structure_id: int,
            attribute_specs: list[AttributeSpec]) -> Structure:
        forest_response = self.rest_api.get_forest(structure_id=structure_id)

        row_ids = [
            component.row_id
            for component in forest_response.components
        ]

        value_response = self.rest_api.get_value(
            forest_response.spec.structure_id,
            row_ids,
            attribute_specs)

        structure = Structure(id=structure_id)

        for value_response_item in value_response.responses:
            # Iterate through row column data
            # for value in value_response_item.data[i_row].values:
            for data_item in value_response_item.data:
                # Which column do we have data for
                attribute_id = data_item.attribute.id
                attribute_spec = (
                    data_item.attribute
                )
                # Store attribute data in resulting structure
                structure.attribute_specs[attribute_id] = attribute_spec

                for i_value, value_item in enumerate(data_item.values):
                    row_id = value_response_item.rows[i_value]
                    # Get existing or create new row
                    structure_row = next(
                        (sr for sr in structure.rows if sr.id == row_id),
                        StructureRow(id=row_id)
                    )
                    is_row_new = (len(structure_row.attribute_ids) == 0)
                    # Add attribute id and value to row data
                    structure_row.attribute_ids.append(attribute_id)
                    structure_row.values.append(value_item)
                    # add row if it's not present yet
                    if is_row_new:
                        structure.rows.append(structure_row)

        return structure
