# JI(ra)ST(ructure)py

Client for accessing Jira [Structure REST API](https://help.tempo.io/structure-dc/latest/structure-rest-api-reference) from python.

## Basic concepts

Client API is exposed through `JIST` instance. Once successfully authenticated, data can be loaded using the following:

- `rest_api` variable - exposes module which contains functions that call low-level Jira Structure REST API endpoints
- `structure(structure_id)` method - creates `Structure` instance with high-level fluent API to setup optional parameters, that are used to load data within structure hierarchy.

Each retrieval of data or API call is wrapped in `JistOperation` object, which provide information about the operation outcome:

- In case of success, retrieved data are present in `content` field.
- In case of failure, `JistError` object in `error` field contains data about reason behind the failure.
- `succeeded` and `failed` properties can be used to check for content or errors presence of the operation.

## Usage examples

### Retrieve structure with specific attributes

```python
from polars as pl
from jist import JIST, AttributeId

# Setup client
secret = load_secret() # Implement secret loading on your own
jist = JIST(hostname=secret.hostname, pat=secret.pat)

# Retrieve structure data with specified attributes
operation = (
    jist.structure(123)
        .with_attribute(AttributeId.SUMMARY)
        .with_attribute(AttributeId.STATUS)
        .with_attribute(AttributeId.LABELS)
        .load()
)

# Print error if operation failed
if operation.failed:
    print(f"Structure data loading error: {operation.error.message}")
    return

# Load data into dictionary
data = {}

for column_id, column in operation.content.columns.items():
    data[column.column_spec.name] = column.values

# Using polars to demonstrate loading data into DataFrame
df = pl.DataFrame(data=data)

# Print DataFrame into console
print(df)
```

## Client API

### JIST class

Top level instance of 

#### Constructor

```python
JIST(
    hostname: str,
    username: str = None,
    password: str = None,
    pat: str = None,
    authentication_mode=AuthenticationMode.PAT
)
```

#### Call low level REST API

Implemented Jira Structure REST API endpoint calls are located under `rest_api` variable which exposes module functions. These calls are described in [REST API endpoints implementation](#rest-api-endpoints-implementation).

#### Retrieve PAT

```python
request_pat(
    username: str,
    password: str
) -> JistOperation[PatResponse]
```

#### Load configuration

```python
load_config() -> JistOperation[ConfigResponse]
```

#### Read structure

```python
structure(
    structure_id: int
) -> Structure
```

### Structure class

Structure class has fluent API, which first allows to setup optional parameters based on which the data will be loaded.

#### Setup of parameters 

```python
with_config(
    apply_config=True
)

with_rows(
    row_ids: list[int]
)

with_row_metadata(
    include_row_metadata=True,
    cache_row_metadata=True
)

with_attribute(
    id: AttributeId,
    format: str = AttributeValueFormat.TEXT
)

with_attribute_spec(
    attribute_spec: AttributeSpec
)

with_attribute_specs(
    attribute_specs: list[AttributeSpec]
)
```

#### Load structure with specified or default view

```python
load_view(
    view_id: int = None
) -> JistOperation[Hierarchy]
```

#### Load structure without view

```python
load() -> JistOperation[Hierarchy]
```

### Hierarchy class

```python
columns: dict[str, Column]
```

```python
get_columns(
    *column_names: str
) -> dict[str, list[any]]
```

### Column class

```python
id: str
columns_spec: ColumnSpec
attribute_spec: AttributeSpec
values: list[any]
```

### ColumnKey enum

```python
ROW_ID = "__row_id"  # Library internal
ROW_DEPTH = "__row_depth"  # Library internal
ROW_ITEM_TYPE = "__row_item_type"  # Library internal
ROW_ITEM_ID = "__row_item_id"  # Library internal
ROW_ISSUE_ID = "__row_issue_id"  # Library internal
KEY = "key"
SUMMARY = "Summary"
ACTIONS = "actions"
FIELD = "field"
FORMULA = "formula"
HANDLE = "handle"
MAIN = "main"
UNKNOWN = "unknown"  # Placeholder value for undetermined column key
```

### AttributeId enum

```python
AFFECTS_VERSIONS = "versions"
ASSIGNEE = "assignee"
COMPONENTS = "components"
CREATED = "created"
CREATOR = "creator"
CUSTOMFIELD = "customfield"
DESCRIPTION = "description"
DISPLAYABLE = "displayable"
DONE = "done"
DUEDATE = "duedate"
EDITABLE = "editable"
FIX_VERSIONS = "fixVersions"
FORMULA = "expr"
ICON = "icon"
ISSUETYPE = "issuetype"
ITEM = "item"
KEY = "key"
LABELS = "labels"
PRIORITY = "priority"
PROGRESS = "progress"
PROJECT = "project"
REPORTER = "reporter"
STATUS = "status"
SUM = "sum"
SUMMARY = "summary"
TYPE = "type"
UNKNOWN = "unknown"  # Determines ID which is not implemented
UPDATED = "updated"
URL = "url"
USER = "user"
VOTES = "votes"
WATCHES = "watches"
```

### AttributeValueFormat enum

```python
ANY = "any"
BOOLEAN = "boolean"
DURATION = "duration"
HTML = "html"
ID = "id"
JSON_ARRAY = "json_array"
JSON_OBJECT = "json"
NUMBER = "number"
ORDER = "order"
TEXT = "text"
TIME = "time"
```

## REST API endpoints implementation

### Structure resourse

#### List structures

- [Official docs](https://help.tempo.io/structure-dc/latest/structure-resource#get)
- Endpoint: `BASEURL/rest/structure/2.0/structure`
- HTTP verb: GET
- Status: Implemented
- Client API:

```python
jist.rest_api.get_structures() -> JistOperation[StructuresResponse]
```

#### Read structure

- [Official docs](https://help.tempo.io/structure-dc/latest/structure-resource#get-id)
- Endpoint: `BASEURL/rest/structure/2.0/structure/{structure_id}`
- HTTP verb: GET
- Status: Implemented
- Client API:

```python
jist.rest_api.get_structure(
    structure_id: int
) -> JistOperation[StructureResponse]
```

### Forest resource

#### Read forest

- [Official docs](https://help.tempo.io/structure-dc/latest/forest-resource#Retrieving-Forest)
- Endpoint: `BASEURL/rest/structure/2.0/forest/latest`
- HTTP verb: POST
- Status: Implemented
- Client API:

```python
jist.rest_api.get_forest(
    structure_id: int
) -> JistOperation[ForestResponse]
```

### Value resource

#### Load values

- [Official docs](https://help.tempo.io/structure-dc/latest/value-resource#Loading-Values)
- Endpoint: `BASEURL/rest/structure/2.0/value`
- HTTP verb: POST
- Status: Implemented
- Client API:

```python
jist.rest_api.get_value(
    structure_id: int,
    rows: list[int],
    attribute_specs: list[AttributeSpec]
) -> JistOperation[ValueResponse]
```

### Attribute subscription resource

#### Create subscription

- [Official docs](https://help.tempo.io/structure-dc/latest/attribute-subscription-resource#AttributeSubscriptionResource-CreateSubscription)
- Endpoint: `BASEURL/rest/structure/2.0/attribute/subscription`
- HTTP verb: POST
- Status: Implemented
- Client API:

```python
jist.rest_api.create_subscription(
    structure_id: int,
    rows: list[int],
    attributes: list[AttributeSpec],
    values_update: bool = False,
    values_timeout: int = 1000
) -> JistOperation[SubscriptionData]
```

#### Read subscription

- [Official docs](https://help.tempo.io/structure-dc/latest/attribute-subscription-resource#AttributeSubscriptionResource-RetrieveSubscriptionorValues)
- Endpoint: `BASEURL/rest/structure/2.0/attribute/subscription/{subscription_id}`
- HTTP verb: GET
- Status: Implemented
- Client API:

```python
jist.rest_api.poll_subscription(
    subscription_id: int,
    signature: int,
    version: int,
    values_update: bool = False,
    values_timeout: int = 1000,
    skip_loading: bool = False
) -> JistOperation[SubscriptionData]
```

#### Delete subscription

- [Official docs](https://help.tempo.io/structure-dc/latest/attribute-subscription-resource#AttributeSubscriptionResource-DeleteSubscription)
- Endpoint: `BASEURL/rest/structure/2.0/attribute/subscription/{subscription_id}`
- HTTP verb: DELETE
- Status: Implemented
- Client API:

```python
jist.rest_api.delete_subscription(
    subscription_id: int
) -> JistOperation[bool]
```

### View resource

#### Read view

- No official docs available (reverse engineered from network traffic).
- Endpoint: `BASEURL/rest/structure/1.0/view/{view_id}`
- HTTP verb: GET
- Status: Implemented
- Client API:

```python
jist.rest_api.get_view(
    view_id: int
) -> JistOperation[ViewResponse]
```

#### Read structure default view

- No official docs available (reverse engineered from network traffic).
- Endpoint: `BASEURL/rest/structure/1.0/view/default?forPage=structure&forStructure={structure_id}`
- HTTP verb: GET
- Status: Implemented
- Client API:

```python
jist.rest_api.get_default_view(
    structure_id: int
) -> JistOperation[ViewResponse]
```

### Configuration resource

#### Read configuration

- No official docs available (reverse engineered from network traffic).
- Endpoint: `BASEURL/rest/structure/1.0/config/widget`
- HTTP verb: GET
- Status: Implemented
- Client API:

```python
jist.rest_api.get_config() -> JistOperation[ConfigResponse]
```

### PAT resource

#### Read PAT

- Jira REST API endpoint to allow authentication via Personal Access Tokens (PATs).
- [Official docs](https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html)
- Endpoint: `BASEURL/rest/pat/latest/tokens`
- HTTP verb: POST
- Status: Implemented
- Client API:

```python
jist.rest_api.get_pat(
    username: str,
    password: str
) -> JistOperation[PatResponse]
```
