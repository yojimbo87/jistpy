from specs import ForestComponent


def parse_formula(formula: str) -> list[ForestComponent]:
    forest_components: list[ForestComponent] = []

    for raw_component in formula.split(","):
        component_parts = raw_component.split(":")

        item_identity = component_parts[2]
        item_type: int = 0
        item_id: str = ""
        issue_id: int = 0
        item_split: list[str] = []

        if "//" in item_identity:
            item_split = item_identity.split("//")
        elif "/" in item_identity:
            item_split = item_identity.split("/")

        if len(item_split) == 2:
            item_type = item_split[0]
            item_id = item_split[1]
        else:
            issue_id = int(item_identity)

        if len(item_split) == 0:
            issue_id = int(item_identity)
        elif len(item_split) == 2:
            item_type = item_split[0]
            item_id = item_split[1]

        forest_components.append(
            ForestComponent(
                raw_component=raw_component,
                row_id=int(component_parts[0]),
                row_depth=int(component_parts[1]),
                row_semantic=(
                    int(component_parts[3])
                    if (len(component_parts) > 3)
                    else 0
                ),
                item_identity=item_identity,
                item_type=item_type,
                item_id=item_id,
                issue_id=issue_id
            )
        )

    return forest_components
