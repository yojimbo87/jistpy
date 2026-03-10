from jist.specs import (
    ConfigResponse,
    JiraConfig
)

jira_config: JiraConfig = None


def load_config(config_response: ConfigResponse):
    global jira_config

    jira_config = JiraConfig(
        structure_version=config_response.structure_version,
        jira_version=config_response.jira_version
    )

    for jira_field in config_response.jira_fields:
        jira_config.fields[jira_field.id] = jira_field
