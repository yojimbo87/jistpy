import jist.utils.http_service as http
from jist.specs import (
    AttributeId,
    AttributeValueFormat,
    JiraConfig,
    AttributeSpec,
    ItemType,
    Structure,
    StructureColumnKey,
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
        structure_columns: list[StructureColumn] = []

        # Create list of attribute specs for retrieval of structure data
        for column_spec in view_response.spec.columns:
            # By default attribute ID is unknown before parsing
            attribute_id = AttributeId.UNKNOWN
            # TODO: for now default format is set to retrieve text
            attribute_format = AttributeValueFormat.TEXT
            attribute_params = {}
            # Column name can be different than attribute ID
            column_name = ""

            # Load column name from spec if it's present
            if column_spec.name:
                column_name = column_spec.name

            # Column spec key can determine attribute data and column name
            match column_spec.key:
                case "main":
                    # Main key represents column which should always be item
                    # summary field
                    attribute_id = AttributeId.SUMMARY
                case "field":
                    # Get field name from column spec
                    field: str = column_spec.params["field"]

                    # If field is customfield attribute
                    if field.startswith("customfield_"):
                        attribute_id = AttributeId.CUSTOMFIELD
                        attribute_params["fieldId"] = field[12:]
                    # In other cases try to parse the field as standard
                    # fieldattribute
                    else:
                        attribute_id = AttributeId(field)

                    # Load column name from config if it's applicable
                    if apply_config:
                        column_name = next(
                            (
                                v.name
                                for k, v in self.jira_config.fields.items()
                                if v.id == attribute_id
                            ),
                            column_spec.name
                        )
                case "formula":
                    attribute_id = AttributeId.FORMULA
                    attribute_params = column_spec.params

            # Create attribute spec based on previously processed data
            attribute_spec = AttributeSpec(
                id=attribute_id,
                format=attribute_format,
                params=attribute_params
            )
            # Add to the list of attribute specs to be sent in request
            attribute_specs.append(attribute_spec)
            # Add to the list of columns to know which row value belongs to
            # which column - nth row value corresponds to nth column definition
            structure_columns.append(
                StructureColumn(
                    csid=column_spec.csid,
                    key=column_spec.key,
                    name=column_name,
                    attribute_spec=attribute_spec
                )
            )

        # Retrieve structure data
        structure = self.load_structure(structure_id, attribute_specs)
        # Once structure data is retrieved and processed into rows, overwrite
        # column definitions based on data retrieved from view
        structure.columns = structure_columns

        return structure

    # Loads structure data for specified attributes
    def load_structure(
            self, structure_id: int,
            attribute_specs: list[AttributeSpec]) -> Structure:
        # Load forest data
        forest_response = self.rest_api.get_forest(structure_id=structure_id)
        # Get row IDs from forest components
        row_ids = [
            component.row_id
            for component in forest_response.components
        ]
        # Load forest values
        value_response = self.rest_api.get_value(
            forest_response.spec.structure_id,
            row_ids,
            attribute_specs
        )
        # Create new structure object into which will be data stored
        structure = Structure(id=structure_id)

        # Iterate through responses
        for value_response_item in value_response.responses:
            # Iterate through response data
            for i_data_item, data_item in enumerate(value_response_item.data):
                # Append column definition based on data index as csid and
                # attribute data retrieved in response
                structure.columns.append(
                    StructureColumn(
                        csid=str(i_data_item),
                        key=StructureColumnKey.UNKNOWN,
                        name=data_item.attribute.id,
                        attribute_spec=data_item.attribute
                    )
                )

                # Iterate through values of specific attribute
                for i_value, value_item in enumerate(data_item.values):
                    # Which row ID is the value for
                    row_id = value_response_item.rows[i_value]
                    # Get forest component data based on value index
                    forest_component = forest_response.components[i_value]
                    # Determine item type
                    item_type = (
                        ItemType.ISSUE
                        if forest_component.issue_id
                        else ItemType.MISSING
                    )
                    item_type_field = str(forest_component.item_type)

                    if (item_type_field in forest_response.item_types):
                        item_type = ItemType(
                            forest_response.item_types[item_type_field]
                        )

                    # Get existing or create new row - this needs to be either
                    # created or loaded from existing rows, because row values
                    # are stored for individual attributes/columns
                    structure_row = next(
                        (sr for sr in structure.rows if sr.id == row_id),
                        StructureRow(
                            id=row_id,
                            depth=forest_component.row_depth,
                            item_type=item_type,
                            item_id=forest_component.item_id,
                            issue_id=forest_component.issue_id
                        )
                    )
                    is_row_new = (len(structure_row.values) == 0)

                    # Add row value
                    structure_row.values.append(value_item)
                    # Add row if it's not present yet
                    if is_row_new:
                        structure.rows.append(structure_row)

        return structure
