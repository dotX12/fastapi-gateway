import pytest
from httpx import AsyncClient
from tests.fastapi_gateway_service.main import app as app_gateway

BASE_URL_MICROSERVICE = "http://gateway.localtest.me:8001"
PREFIX_GATEWAY = "/gateway_endpoint"
URL = BASE_URL_MICROSERVICE + PREFIX_GATEWAY


@pytest.mark.asyncio
async def test_check_path_param_get():
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.get(
            url="/path_param/1337",
        )
    assert response_success.status_code == 200
    assert response_success.json() == {"custom_int": "1337", "foo": "bar"}

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_bad = await client.get(
            url="/path_param/not_integer",
        )
    assert response_bad.status_code == 422
    assert response_bad.json() == {
        "detail": [
            {
                "loc": ["path", "random_int"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }


@pytest.mark.asyncio
async def test_check_path_param_and_body_post():
    example_body = {"example_int": 12345, "example_str": "string_1234"}

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.post(
            url="/path_and_body/1337", json=example_body
        )
    assert response_success.status_code == 200
    assert response_success.json() == {
        "example_int": 12345,
        "example_str": "string_1234",
        "foo": "bar",
        "path_int": 1337,
    }

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_without_body_path = await client.post(
            url="/path_and_body/not_integer",
        )
    assert response_without_body_path.status_code == 422
    assert response_without_body_path.json() == {
        "detail": [
            {
                "loc": ["path", "path_int"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            },
            {"loc": ["body"], "msg": "field required", "type": "value_error.missing"},
        ]
    }

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_without_path = await client.post(
            url="/path_and_body/foo", json=example_body
        )
    assert response_without_path.status_code == 422
    assert response_without_path.json() == {
        "detail": [
            {
                "loc": ["path", "path_int"],
                "msg": "value is not a valid integer",
                "type": "type_error.integer",
            }
        ]
    }

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_without_body = await client.post(
            url="/path_and_body/512",
        )
    assert response_without_body.status_code == 422
    assert response_without_body.json() == {
        "detail": [
            {"loc": ["body"], "msg": "field required", "type": "value_error.missing"}
        ]
    }


@pytest.mark.asyncio
async def test_check_list_response_get():
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response = await client.get("/list_model")
    assert response.status_code == 200
    assert response.json() == [{"foo_key": "foo"}, {"foo_key": "bar"}]


@pytest.mark.asyncio
async def test_query_params_post():
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        query_params = {"query_int": 999, "query_str": "TemplateString"}
        response = await client.get("/query", params=query_params)

    assert response.status_code == 200
    assert response.json() == {"query_int": 999, "query_str": "TemplateString"}


@pytest.mark.asyncio
async def test_query_body_post():
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        example_query = {"query_int": 9991, "query_str": "TemplateString!"}
        example_body = {"example_int": 9888, "example_str": "foo_bar"}

        response = await client.post(
            "/query_and_body", params=example_query, json=example_body
        )

    assert response.status_code == 200
    assert response.json() == {
        "example_int": 9888,
        "example_str": "foo_bar",
        "query_int": 9991,
        "query_str": "TemplateString!",
    }


@pytest.mark.asyncio
async def test_query_body_path_post():
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        query_params = {"query_int": 12000, "query_str": "query_str0"}
        body_params = {"example_int": 9888, "example_str": "example_body_str"}
        response = await client.post(
            "/query_and_body_path/981", params=query_params, json=body_params
        )

    assert response.status_code == 200
    assert response.json() == {
        "example_int": 9888,
        "example_str": "example_body_str",
        "path": 981,
        "query_int": 12000,
        "query_str": "query_str0",
    }


@pytest.mark.asyncio
async def test_dependency_gateway_post():
    headers = {"x-api-key": "EXAMPLE_HEADER"}
    async with AsyncClient(app=app_gateway, base_url=URL, headers=headers) as client:
        response_success = await client.get("/check_depends_header")
    assert response_success.status_code == 200
    assert response_success.json() == {"foo": "bar", "header": "EXAMPLE_HEADER"}

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_bad = await client.get("/check_depends_header")
    assert response_bad.status_code == 401
    assert response_bad.json() == {
        "detail": "You didn't pass the api key in the header! Header: x-api-key"
    }


@pytest.mark.asyncio
async def test_form_data_post():
    form_data = {"username": "ivanov124", "password": "pwd123456789"}
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.post("/form_data", data=form_data)
    assert response_success.status_code == 200
    assert response_success.json() == {
        "foo": "bar",
        "password": "pwd123456789",
        "username": "ivanov124",
    }

    form_data = {"username": "ivanov124"}
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_bad = await client.post("/form_data", data=form_data)
    assert response_bad.status_code == 422
    assert response_bad.json() == {
        "detail": [
            {
                "loc": ["body", "password"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


@pytest.mark.asyncio
async def test_upload_file_post():
    file_rb = {"file": ("example_photo.jpg", open("src/photo.jpg", "rb"))}
    file_r = {"file": ("example_photo.jpg", open("src/photo.jpg", "r"))}

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.post("/upload_file", files=file_rb)
    assert response_success.status_code == 200
    assert response_success.json() == {
        "filename": "example_photo.jpg",
        "file_content_type": "image/jpeg",
    }

    with pytest.raises(TypeError):
        async with AsyncClient(app=app_gateway, base_url=URL) as client:
            response_success = await client.post("/upload_file", files=file_r)
        # assert response_success.status_code == 400
        # assert response_success.json() == {"detail": "There was an error parsing the body"}


@pytest.mark.asyncio
async def test_upload_file_form_data_post():
    form_data = {"username": "ivanov124", "password": "pwd123456789"}
    file = {"file": ("example_photo.jpg", open("src/photo.jpg", "rb"))}

    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.post(
            url="/form_and_upload_file",
            data=form_data,
            files=file,
        )
    assert response_success.status_code == 200
    assert response_success.json() == {
        "content_type": "image/jpeg",
        "filename": "example_photo.jpg",
        "pwd": "pwd123456789",
        "username": "ivanov124",
    }


@pytest.mark.asyncio
async def test_unpack_dependency_form():
    form_data = {"username": "ivanov124", "password": "pwd123456789"}
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.post(
            url="/check_depends_form_1",
            data=form_data,
        )
    assert response_success.status_code == 200
    assert response_success.json() == form_data


@pytest.mark.asyncio
async def test_unpack_dependency_form_2():
    form_data = {"username": "user111", "password": "password222"}
    async with AsyncClient(app=app_gateway, base_url=URL) as client:
        response_success = await client.post(
            url="/check_depends_form_2",
            data=form_data,
        )
    assert response_success.status_code == 200
    assert response_success.json() == form_data
