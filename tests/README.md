## - How to run tests?

To begin with, we raise our test microservice and the gateway.
```
cd tests
uvicorn "fastapi_gateway_service.main:app" --host "gateway.localtest.me" --port 8001
uvicorn "fastapi_microservice.main:app" --host "microservice.localtest.me" --port 8002
```

And run tests.
```
pytest test.py
```

### - Test results:
```
platform darwin -- Python 3.9.2, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/boot/Documents/Python/fastapi-gateway/tests
plugins: asyncio-0.15.1, anyio-3.3.0, web3-5.23.0

============================= test session starts ==============================
collecting ... collected 10 items

test.py::test_check_path_param_GET PASSED                                [ 10%]
test.py::test_check_path_param_and_body_POST PASSED                      [ 20%]
test.py::test_check_list_response_GET PASSED                             [ 30%]
test.py::test_query_params_GET PASSED                                    [ 40%]
test.py::test_query_body_POST PASSED                                     [ 50%]
test.py::test_query_body_path_POST PASSED                                [ 60%]
test.py::test_dependency_gateway_GET PASSED                              [ 70%]
test.py::test_form_data_POST PASSED                                      [ 80%]
test.py::test_upload_file_POST PASSED                                    [ 90%]
test.py::test_upload_file_form_data_POST PASSED                          [100%]

============================== 10 passed in 0.84s ==============================
```
