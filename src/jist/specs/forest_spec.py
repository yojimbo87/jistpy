from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


# https://apidocs.tempo.io/dc-structure/javadoc/structure/latest/com/almworks/jira/structure/api/item/CoreItemTypes.html
# https://apidocs.tempo.io/dc-structure/javadoc/structure/latest/constant-values.html
class ItemType(str, Enum):
    ARTIFICIAL = "com.almworks.jira.structure:type-planning-task"
    ATTACHMENT = "com.almworks.jira.structure:type-attachment"
    BOARD = "com.almworks.jira.structure:type-board"
    CF_OPTION = "com.almworks.jira.structure:type-cf-option"
    CHANGE_HISTORY_GROUP = "com.almworks.jira.structure:type-change-history-group"  # noqa: E501
    CHANGE_HISTORY_ITEM = "com.almworks.jira.structure:type-change-history-item"  # noqa: E501
    COMMENT = "com.almworks.jira.structure:type-comment"
    COMPONENT = "com.almworks.jira.structure:type-project-component"
    DATE = "com.almworks.jira.structure:type-date"
    EFFECTOR = "com.almworks.jira.structure:type-effector"
    FOLDER = "com.almworks.jira.structure:type-folder"
    GENERATOR = "com.almworks.jira.structure:type-generator"
    GROUP = "com.almworks.jira.structure:type-group"
    INSIGHT_OBJECT = "com.almworks.jira.structure:type-insight-object"
    ISSUE = "com.almworks.jira.structure:type-issue"
    ISSUE_LINK = "com.almworks.jira.structure:type-issue-link"
    ISSUE_LINK_TYPE = "com.almworks.jira.structure:type-issue-link-type"
    ISSUETYPE = "com.almworks.jira.structure:type-issuetype"
    LABEL = "com.almworks.jira.structure:type-label"
    LOOP_MARKER = "com.almworks.jira.structure:type-loop-marker"
    MEMO = "com.almworks.jira.structure:type-memo"
    MEMO_CHANGE_HISTORY_GROUP = "com.almworks.jira.structure:type-memo-change-history-group"  # noqa: E501
    MISSING = "com.almworks.jira.structure:type-missing"
    PLANNING_TASK = "com.almworks.jira.structure:type-planning-task"
    PRIORITY = "com.almworks.jira.structure:type-priority"
    PROJECT = "com.almworks.jira.structure:type-project"
    PROJECT_CATEGORY = "com.almworks.jira.structure:type-project-category"
    REMOTE_LINK = "com.almworks.jira.structure:type-remote-link"
    REQUEST_TYPE = "com.almworks.jira.structure:type-sd-request-type"
    RESOLUTION = "com.almworks.jira.structure:type-resolution"
    SPRINT = "com.almworks.jira.structure:type-sprint"
    STANDARD_TYPE_PREFIX = "com.almworks.jira.structure:type-"
    STATUS = "com.almworks.jira.structure:type-status"
    STRUCTURE = "com.almworks.jira.structure:type-structure"
    STRUCTURE_VERSION = "com.almworks.jira.structure:type-structure-version"
    TEMPO_ACCOUNT = "com.almworks.jira.structure:type-tempo-account"
    USER = "com.almworks.jira.structure:type-user"
    VERSION = "com.almworks.jira.structure:type-version"
    VERSION_NAME = "com.almworks.jira.structure:type-version-name"
    WORKLOG = "com.almworks.jira.structure:type-worklog"


class ForestSpec(BaseModel):
    structure_id: int = Field(alias="structureId")

    model_config = ConfigDict(serialize_by_alias=True, populate_by_name=True)


class Version(BaseModel):
    signature: int
    version: int


class ForestComponent(BaseModel):
    raw_component: str
    row_id: int
    row_depth: int
    item_identity: str
    row_semantic: int
    item_type: int
    item_id: str
    issue_id: int


class ForestResponse(BaseModel):
    spec: ForestSpec
    formula: str
    components: list[ForestComponent] = Field(default=None)
    item_types: dict = Field(alias="itemTypes")
    version: Version
