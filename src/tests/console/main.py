import polars as pl
# from devtools import pprint
from jist import JIST, AttributeId
from jist.utils import Secret


def main():
    secret = Secret("../../secret.ini", "Credentials2")
    jist = JIST(hostname=secret.hostname, pat=secret.pat)

    # Retrieve structure data with specified attributes
    operation = (
        jist.structure(613)
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
    # data = jist.get_structure(600)
    # data = jist.get_forest(600)

    # pprint(data)


if __name__ == '__main__':
    main()
