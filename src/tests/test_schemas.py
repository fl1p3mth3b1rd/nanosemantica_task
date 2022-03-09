import pytest
from marshmallow.exceptions import ValidationError

from src.schemas import (
    AllParamsRequestSchema,
    GeneralResponseSchema,
    ByNameRequestSchema,
    ByAgeRequestSchema,
    ByDepartmentRequestSchema,
    UpdateRequestSchema
)


def test_all_params_request_schema():
    """Тест на сериализацию объекта входного запроса схемой AllParamsRequestSchema."""
    request_correct = {
        'name': 'Артур',
        'age': 25,
        'department': 'department_1'
    }
    AllParamsRequestSchema().load(request_correct)
    request_incorrect = {
        'this_is': 'empty',
    }
    with pytest.raises(ValidationError):
        AllParamsRequestSchema().load(request_incorrect)

def test_by_name_request_schema():
    """Тест на сериализацию объекта входного запроса схемой ByNameRequestSchema."""
    request_correct = {
        'name': 'Артур'
    }
    ByNameRequestSchema().load(request_correct)
    request_incorrect = {
        'this_is': 'empty',
    }
    with pytest.raises(ValidationError):
        ByNameRequestSchema().load(request_incorrect)

def test_by_age_request_schema():
    """Тест на сериализацию объекта входного запроса схемой ByAgeRequestSchema."""
    request_correct = {
        'age': 25
    }
    ByAgeRequestSchema().load(request_correct)
    request_incorrect = {
        'this_is': 'empty',
    }
    with pytest.raises(ValidationError):
        ByAgeRequestSchema().load(request_incorrect)

def test_by_department_request_schema():
    """Тест на сериализацию объекта входного запроса схемой ByDepartmentRequestSchema."""
    request_correct = {
        'department': 'Отдел 1'
    }
    ByDepartmentRequestSchema().load(request_correct)
    request_incorrect = {
        'this_is': 'empty',
    }
    with pytest.raises(ValidationError):
        ByDepartmentRequestSchema().load(request_incorrect)
    
def test_update_request_schema():
    """Тест на сериализацию объекта входного запроса схемой UpdateRequestSchema."""
    request_correct = {
        'name': 'Артур',
        'age': 25,
        'department': 'department_1',
        'new_name': 'Новое имя',
        'new_age': 26,
        'new_department': 'Новый отдел',
    }
    UpdateRequestSchema().load(request_correct)
    request_incorrect = {
        'this_is': 'empty',
    }
    with pytest.raises(ValidationError):
        UpdateRequestSchema().load(request_incorrect)

def test_general_response_schema():
    """Тест на сериализацию объекта входного запроса схемой GeneralResponseSchema."""
    request_correct = {
        'error': False,
        'status_code': 200,
        'message': 'Ok',
        'payload': 'some payload'
    }
    GeneralResponseSchema().load(request_correct)
    request_incorrect = {
        'this_is': 'empty',
    }
    with pytest.raises(ValidationError):
        GeneralResponseSchema().load(request_incorrect)
