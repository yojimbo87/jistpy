# JI(ra)ST(ructure)py

Client for accessing JIRA Structure REST API from python.

## Usage

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