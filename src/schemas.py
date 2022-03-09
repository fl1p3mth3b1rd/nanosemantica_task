from dataclasses import dataclass, field
from typing import Optional
from http import HTTPStatus

import marshmallow
from marshmallow_dataclass import class_schema


@dataclass
class AllParamsRequest:
    name: str
    age: int = field(metadata={
        "marshmallow_field": marshmallow.fields.Integer(
            required=True, 
            strict=True, 
            validate=marshmallow.validate.Range(min=18, max=70)
        )
    })
    department: str


@dataclass
class ByNameRequest:
    name: str


@dataclass
class ByAgeRequest:
    age: int


@dataclass
class ByDepartmentRequest:
    department: str


@dataclass
class UpdateRequest(AllParamsRequest):
    new_name: str
    new_age: int = field(metadata={
        "marshmallow_field": marshmallow.fields.Integer(
            required=True, 
            strict=True, 
            validate=marshmallow.validate.Range(min=18, max=70)
        )
    })
    new_department: str


@dataclass
class GeneralResponse:
    error: bool
    status_code: int = field(metadata={
        "marshmallow_field":  marshmallow.fields.Integer(
        required=True,
        strict=True,
        default=None, 
        validate=marshmallow.validate.Range(min=HTTPStatus.OK, max=600)
    )})
    message: str
    payload: Optional[str] = ''


AllParamsRequestSchema = class_schema(AllParamsRequest)
ByNameRequestSchema = class_schema(ByNameRequest)
ByAgeRequestSchema = class_schema(ByAgeRequest)
ByDepartmentRequestSchema = class_schema(ByDepartmentRequest)
UpdateRequestSchema = class_schema(UpdateRequest)
GeneralResponseSchema = class_schema(GeneralResponse)
