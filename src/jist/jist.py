import jist.utils.http_service as http
from jist.specs import (
    JiraConfig,
    AttributeSpec,
    Structure,
    StructureColumn,
    StructureRow
)
from jist.rest_resources import rest_api


class JIST:
    def __init__(self, host: str, username: str, password: str):
        http.init(host, username, password)

        self.rest_api: rest_api = rest_api
        self.jira_config: JiraConfig = None

    def load_config(self) -> None:
        config_response = self.rest_api.get_config()

        self.jira_config = JiraConfig(
            structure_version=config_response.structure_version,
            jira_version=config_response.jira_version
        )

        for jira_field in config_response.jira_fields:
            self.jira_config.fields[jira_field.id] = jira_field

    # Loads structure data with default view attributes
    def load_structure_view(
            self,
            structure_id: int,
            apply_config: bool = True) -> Structure:
        view_response = self.rest_api.get_default_view(structure_id)

        # Check whether we should use config
        if (apply_config and self.jira_config is None):
            self.load_config()

        attribute_specs: list[AttributeSpec] = []

        # Create list of attribute specs for retrieval of structure data
        for column_spec in view_response.spec.columns:
            attribute_id: str = ""
            attribute_format = "text"
            attribute_params: dict = {}

            # Determine attribute id based on column key
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

        # Retrieve structure data
        structure = self.load_structure(structure_id, attribute_specs)

        # Create column definitions for structure data
        for column_spec in view_response.spec.columns:
            column_name: str = ""
            attribute_id: str = ""

            # If column has name in it's spec
            if (column_spec.name):
                column_name = column_spec.name
            # If column is field
            elif ((column_spec.key == "field") and
                  ("field" in column_spec.params)):
                # Determine attribute id from column spec params field
                attribute_id = next(
                    atts.id
                    for atts in attribute_specs
                    if atts.id == column_spec.params["field"]
                )

                # Load column name from config if it's applicable
                if apply_config:
                    column_name = next(
                        v.name
                        for k, v in self.jira_config.fields.items()
                        if v.id == attribute_id
                    )
            # If column is formula
            elif (column_spec.key == "formula"):
                # Name of the formula is located in name field
                column_name = column_spec.name

            structure.columns[column_spec.csid] = StructureColumn(
                csid=column_spec.csid,
                key=column_spec.key,
                name=column_name,
                attribute_id=attribute_id
            )

        return structure

    # Loads structure data for specified attributes
    def load_structure(
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
            # Iterate through row attributes
            for i_data, data_item in enumerate(value_response_item.data):
                # Which attribute do we have data for
                attribute_id = data_item.attribute.id
                attribute_spec = (
                    data_item.attribute
                )
                # Store attribute data in resulting structure
                structure.attribute_specs.append(attribute_spec)

                # Iterate through values of specific attribute
                for i_value, value_item in enumerate(data_item.values):
                    # Which row is the value for
                    row_id = value_response_item.rows[i_value]
                    # Get existing or create new row
                    structure_row = next(
                        (sr for sr in structure.rows if sr.id == row_id),
                        StructureRow(id=row_id)
                    )
                    is_row_new = (len(structure_row.attribute_ids) == 0)
                    # Add metadata and value to resulting structure row
                    structure_row.csids.append(i_data + 1)
                    structure_row.attribute_ids.append(attribute_id)
                    structure_row.values.append(value_item)
                    # add row if it's not present yet
                    if is_row_new:
                        structure.rows.append(structure_row)

        return structure
