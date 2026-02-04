from jist.specs import AttributeValueFormat, JiraFieldType


def parse_attribute_format(jira_field_type: str) -> str:
    value_format: str = AttributeValueFormat.text

    match jira_field_type:
        case JiraFieldType.any:
            value_format = AttributeValueFormat.any
        case JiraFieldType.array:
            value_format = AttributeValueFormat.json_array
        case (JiraFieldType.date |
                JiraFieldType.datetime):
            value_format = AttributeValueFormat.time
        case JiraFieldType.number:
            value_format = AttributeValueFormat.number
        case (JiraFieldType.string |
                JiraFieldType.custom |
                JiraFieldType.option |
                JiraFieldType.priority |
                JiraFieldType.progress |
                JiraFieldType.project |
                JiraFieldType.resolution |
                JiraFieldType.security_level |
                JiraFieldType.status |
                JiraFieldType.user |
                JiraFieldType.votes |
                JiraFieldType.watches):
            value_format = AttributeValueFormat.text

    return value_format
