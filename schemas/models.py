from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from enum import Enum


class FieldType(str, Enum):
    string = "string"
    integer = "integer"
    float_ = "float"
    boolean = "boolean"
    datetime = "datetime"
    enum = "enum"
    foreign_key = "foreign_key"
    text = "text"
    json = "json"
    array = "array"


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ComponentType(str, Enum):
    table = "table"
    form = "form"
    card = "card"
    chart = "chart"
    list_ = "list"
    modal = "modal"
    button = "button"
    text = "text"
    nav = "nav"


class IntentEntity(BaseModel):
    name: str
    description: str
    attributes: list[str]


class UserRole(BaseModel):
    name: str
    permissions: list[str]


class Feature(BaseModel):
    name: str
    description: str
    requires_auth: bool
    roles_allowed: list[str]


class IntentOutput(BaseModel):
    app_name: str
    app_type: str
    entities: list[IntentEntity]
    roles: list[UserRole]
    features: list[Feature]
    integrations: list[str]
    assumptions: list[str]


class DesignEntity(BaseModel):
    name: str
    description: str
    attributes: list[str] = Field(default_factory=list)


class DesignRelationship(BaseModel):
    name: str
    description: str
    from_entity: Optional[str] = None
    to_entity: Optional[str] = None
    type: Optional[str] = None


class DesignPage(BaseModel):
    name: str
    path: str
    description: str = ""
    access_roles: list[str] = Field(default_factory=list)


class Endpoint(BaseModel):
    method: str
    path: str
    description: str


class APIGroup(BaseModel):
    name: str
    description: str = ""
    endpoints: list[Endpoint] = Field(default_factory=list)


class DesignFlow(BaseModel):
    name: str
    steps: list[str] = Field(default_factory=list)

    @field_validator("steps", mode="before")
    @classmethod
    def coerce_steps(cls, value):
        if not isinstance(value, list):
            return value

        cleaned = []

        for step in value:
            if isinstance(step, str):
                cleaned.append(step)
            elif isinstance(step, dict):
                cleaned.append(
                    step.get("action")
                    or step.get("description")
                    or step.get("page")
                    or str(step)
                )
            else:
                cleaned.append(str(step))

        return cleaned


class SystemDesignOutput(BaseModel):
    entities: list[DesignEntity]
    relationships: list[DesignRelationship]
    pages: list[DesignPage]
    api_groups: list[APIGroup]
    flows: list[DesignFlow]


# =========================
# STAGE 3A: DATABASE
# =========================

class DBField(BaseModel):
    name: str
    type: str
    required: bool = True
    unique: bool = False
    default: Optional[str] = None

    # accepts both:
    # "users(id)"
    # {"table":"users","column":"id"}
    references: Any = None

    enum_values: Optional[list[str]] = None


class DBTable(BaseModel):
    name: str
    fields: list[DBField]

    # accepts both strings and objects
    indexes: list[Any] = Field(default_factory=list)


class DBSchema(BaseModel):
    tables: list[DBTable]


from typing import Optional

class APIField(BaseModel):
    name: str
    type: FieldType
    required: bool = True
    source: Optional[str] = None

    @field_validator("type", mode="before")
    @classmethod
    def fix_type(cls, v):
        if v == "number":
            return "float"
        return v


class APIEndpoint(BaseModel):
    path: str
    method: HttpMethod
    summary: str
    roles_allowed: list[str]
    request_fields: list[APIField]
    response_fields: list[APIField]
    auth_required: bool = True


class APISchema(BaseModel):
    base_path: str
    endpoints: list[APIEndpoint]


class UIField(BaseModel):

    name: Optional[str] = None
    label: Optional[str] = None
    type: Optional[str] = "text"
    required: bool = False
    maps_to_api_field: Optional[str] = None

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):

        if isinstance(obj, str):
            obj = {
                "name": obj,
                "label": obj.title(),
                "type": "text",
                "maps_to_api_field": obj
            }

        elif isinstance(obj, dict):

            obj.setdefault("name", obj.get("id", "field"))
            obj.setdefault("label", obj["name"].title())
            obj.setdefault("type", "text")
            obj.setdefault("maps_to_api_field", obj["name"])

        return super().model_validate(obj, *args, **kwargs)


class UIComponent(BaseModel):
    id: str = ""
    type: str = "card"
    title: str = ""

    fields: list = Field(default_factory=list)

    data_source: Optional[str] = None
    roles_visible: list[str] = Field(default_factory=list)


class UIPage(BaseModel):
    name: str
    path: str

    roles_allowed: list[str] = Field(default_factory=list)

    components: list[UIComponent] = Field(default_factory=list)

    layout: str = "default"


class UISchema(BaseModel):
    pages: list[UIPage] = Field(default_factory=list)

    nav_items: list[dict] = Field(default_factory=list)

    entities: list[dict] = Field(default_factory=list)

    relationships: list[dict] = Field(default_factory=list)

    flows: list[dict] = Field(default_factory=list)


class Permission(BaseModel):
    resource: str
    actions: list[str]


class RoleDefinition(BaseModel):
    name: str
    permissions: list[Permission]
    can_access_pages: list[str]


class AuthSchema(BaseModel):
    strategy: str
    token_expiry_seconds: int
    roles: list[RoleDefinition]
    public_routes: list[str]


class AppConfig(BaseModel):
    intent: IntentOutput
    system_design: SystemDesignOutput
    db_schema: DBSchema
    api_schema: APISchema
    ui_schema: UISchema
    auth_schema: AuthSchema


class ValidationError(BaseModel):
    layer: str
    error_type: str
    detail: str
    fixable: bool = True


class ValidationReport(BaseModel):
    passed: bool
    errors: list[ValidationError]