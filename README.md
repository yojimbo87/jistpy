# JI(ra)ST(ructure)py

Client for accessing Jira [Structure REST API](https://help.tempo.io/structure-dc/latest/structure-rest-api-reference) from python.

## Usage examples

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

# Create polars DataFrame
df = pl.DataFrame(data=data)

# Print DataFrame into console
print(df)
```

## Status of REST API endpoints implementation

Below is a list of REST API endpoints implemented by the client:

| HTTP verb and Endpoint                                                                      | Implementation status |
| :------------------------------------------------------------------------------------------ | :-------------------: |
| GET `BASEURL/rest/structure/2.0/structure`                                                  | [x]                   |
| GET `BASEURL/rest/structure/2.0/structure/{structure_id}`                                   | [x]                   |
| POST `BASEURL/rest/structure/2.0/forest/latest`                                             | [x]                   |
| GET `BASEURL/rest/structure/1.0/view/{view_id}`                                             | [x]                   |
| GET `BASEURL/rest/structure/1.0/view/default?forPage=structure&forStructure={structure_id}` | [x]                   |
| POST `BASEURL/rest/structure/2.0/value`                                                     | [x]                   |
| POST `BASEURL/rest/structure/2.0/attribute/subscription`                                    | [x]                   |
| GET `BASEURL/rest/structure/2.0/attribute/subscription/{subscription_id}`                   | [x]                   |
| DELETE `BASEURL/rest/structure/2.0/attribute/subscription/{subscription_id}`                | [x]                   |
| GET `BASEURL/rest/structure/1.0/config/widget`                                              | [x]                   |
| POST `BASEURL/rest/pat/latest/tokens`                                                       | [x]                   |
