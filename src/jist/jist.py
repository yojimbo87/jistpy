from .structure import StructureColumn, Structure
import jist.utils.http_service as http
from jist.specs import (
    AttributeId,
    AttributeValueFormat,
    JiraConfig,
    AttributeSpec,
    ItemType,
    ColumnKey,
    ColumnSpec,
    ConfigResponse
)
from jist.rest_resources import rest_api
from jist.jist_operation import JistOperation


class JIST:
    def __init__(self, host: str, username: str, password: str):
        http.init(host, username, password)

        self.rest_api: rest_api = rest_api
        self.jira_config: JiraConfig = None

    def load_config(self) -> JistOperation[ConfigResponse]:
        config_operation = self.rest_api.get_config()

        if config_operation.is_success is False:
            return config_operation

        self.jira_config = JiraConfig(
            structure_version=config_operation.content.structure_version,
            jira_version=config_operation.content.jira_version
        )

        for jira_field in config_operation.content.jira_fields:
            self.jira_config.fields[jira_field.id] = jira_field

        return config_operation

    # Loads structure data with default view attributes
    def load_structure_view(
            self,
            structure_id: int,
            apply_config: bool = True) -> JistOperation[Structure]:
        operation = JistOperation[Structure](status_code=0)
        view_operation = self.rest_api.get_default_view(structure_id)

        if view_operation.is_success is False:
            operation.status_code = view_operation.status_code
            operation.error = view_operation.error
            return operation

        # Check whether we should use config
        if (apply_config and self.jira_config is None):
            config_operation = self.load_config()

            if config_operation.is_success is False:
                operation.status_code = config_operation.status_code
                operation.error = config_operation.error
                return operation

        attribute_specs: dict[str, AttributeSpec] = {}
        column_specs: dict[str, ColumnSpec] = {}

        # Create list of attribute specs for retrieval of structure data
        for i, column_spec in enumerate(view_operation.content.spec.columns):
            # By default attribute ID is unknown before parsing
            attribute_id = AttributeId.UNKNOWN
            # TODO: for now default format is set to retrieve text
            attribute_format = AttributeValueFormat.TEXT
            attribute_params = {}
            # Column name can be different than attribute ID
            column_name = ""

            # Column spec key can determine attribute data and column name
            match column_spec.key:
                case ColumnKey.HANDLE:
                    # Handle key should? represent column with issue key
                    attribute_id = AttributeId.KEY
                case ColumnKey.MAIN:
                    # Main key should? represetn column with item summary/name
                    attribute_id = AttributeId.SUMMARY
                    column_name = "Summary"
                case ColumnKey.FIELD:
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
                case ColumnKey.FORMULA:
                    attribute_id = AttributeId.FORMULA
                    attribute_params = column_spec.params

            # Load column name from spec if it's present
            if column_spec.name:
                column_name = column_spec.name
            # If column name is still empty, set the value to attribute ID
            elif not column_name:
                column_name = attribute_id

            # Create attribute spec based on previously processed data
            attribute_spec = AttributeSpec(
                id=attribute_id,
                format=attribute_format,
                params=attribute_params
            )

            column_id = str(i)
            # Add attribute spec which will be sent in the request
            attribute_specs[column_id] = attribute_spec
            # Create and add new column spec
            column_specs[column_id] = ColumnSpec(
                csid=column_spec.csid,
                key=column_spec.key,
                name=column_name,
                params=column_spec.params
            )

        # Retrieve structure data
        operation = self.load_structure(
            structure_id,
            [v for k, v in attribute_specs.items()]
        )

        if operation.is_success is False:
            return operation

        # Copy column and attribute specs from view to column data
        for column_id, column in operation.content.columns.items():
            if column_id in column_specs:
                column.column_spec = column_specs[column_id]
                column.attribute_spec = attribute_specs[column_id]

        return operation

    # Loads structure data for specified attributes
    def load_structure(
            self,
            structure_id: int,
            attribute_specs: list[AttributeSpec]) -> JistOperation[Structure]:
        operation = JistOperation[Structure](status_code=0)
        # Load forest data
        forest_operation = self.rest_api.get_forest(structure_id=structure_id)

        if forest_operation.is_success is False:
            operation.status_code = forest_operation.status_code
            operation.error = forest_operation.error
            return operation

        # Get row IDs from forest components
        row_ids = [
            component.row_id
            for component in forest_operation.content.components
        ]
        # Load forest values
        value_operation = self.rest_api.get_value(
            forest_operation.content.spec.structure_id,
            row_ids,
            attribute_specs
        )

        if value_operation.is_success is False:
            operation.status_code = value_operation.status_code
            operation.error = value_operation.error
            return operation

        # Create new structure object into which will be data stored
        structure = Structure(id=structure_id)

        # Iterate through responses
        for value_response_item in value_operation.content.responses:
            # Create separate data columns for row metedata
            row_ids: list[int] = []
            row_depths: list[int] = []
            row_item_types: list[ItemType] = []
            row_item_ids: list[str] = []
            row_issue_ids: list[int] = []

            # Load row definition data into dedicated data columns by
            # iterating through individual row IDs
            for i_row, row_id in enumerate(value_response_item.rows):
                # Get forest component data based on row ID index
                forest_component = forest_operation.content.components[i_row]
                # Determine item type
                item_type = (
                    ItemType.ISSUE
                    if forest_component.issue_id
                    else ItemType.MISSING
                )
                item_type_field = str(forest_component.item_type)

                if (item_type_field in forest_operation.content.item_types):
                    item_type = ItemType(
                        forest_operation.content.item_types[item_type_field]
                    )

                # Store individual row metadata into dedicated data columns
                row_ids.append(row_id)
                row_depths.append(forest_component.row_depth)
                row_item_types.append(item_type.name)
                row_item_ids.append(forest_component.item_id)
                row_issue_ids.append(forest_component.issue_id)

            structure.columns[ColumnKey.ROW_ID] = StructureColumn(
                id=ColumnKey.ROW_ID,
                columns_spec=ColumnSpec(
                    key=ColumnKey.ROW_ID,
                    name=ColumnKey.ROW_ID,
                    csid=ColumnKey.ROW_ID,
                    params={}
                ),
                attribute_spec=None,
                values=row_ids
            )

            structure.columns[ColumnKey.ROW_DEPTH] = StructureColumn(
                id=ColumnKey.ROW_DEPTH,
                columns_spec=ColumnSpec(
                    key=ColumnKey.ROW_DEPTH,
                    name=ColumnKey.ROW_DEPTH,
                    csid=ColumnKey.ROW_DEPTH,
                    params={}
                ),
                attribute_spec=None,
                values=row_depths
            )

            structure.columns[ColumnKey.ROW_ITEM_TYPE] = StructureColumn(
                id=ColumnKey.ROW_ITEM_TYPE,
                columns_spec=ColumnSpec(
                    key=ColumnKey.ROW_ITEM_TYPE,
                    name=ColumnKey.ROW_ITEM_TYPE,
                    csid=ColumnKey.ROW_ITEM_TYPE,
                    params={}
                ),
                attribute_spec=None,
                values=row_item_types
            )

            structure.columns[ColumnKey.ROW_ITEM_ID] = StructureColumn(
                id=ColumnKey.ROW_ITEM_ID,
                columns_spec=ColumnSpec(
                    key=ColumnKey.ROW_ITEM_ID,
                    name=ColumnKey.ROW_ITEM_ID,
                    csid=ColumnKey.ROW_ITEM_ID,
                    params={}
                ),
                attribute_spec=None,
                values=row_item_ids
            )

            structure.columns[ColumnKey.ROW_ISSUE_ID] = StructureColumn(
                id=ColumnKey.ROW_ISSUE_ID,
                columns_spec=ColumnSpec(
                    key=ColumnKey.ROW_ISSUE_ID,
                    name=ColumnKey.ROW_ISSUE_ID,
                    csid=ColumnKey.ROW_ISSUE_ID,
                    params={}
                ),
                attribute_spec=None,
                values=row_issue_ids
            )

            # Iterate through attributes from response
            for i_data_item, data_item in enumerate(value_response_item.data):
                column_id = str(i_data_item)
                structure.columns[column_id] = StructureColumn(
                    id=str(i_data_item),
                    columns_spec=ColumnSpec(
                        key=ColumnKey.UNKNOWN,
                        name=data_item.attribute.id,
                        csid=str(i_data_item),
                        params={}
                    ),
                    attribute_spec=data_item.attribute,
                    values=data_item.values
                )

        operation.content = structure

        return operation
