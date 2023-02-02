import functools
from aiohttp import ContentTypeError, ClientConnectorError
from fastapi import Request, Response, HTTPException, status, params
from typing import List, Optional, Sequence, Dict, Union, Any, Type
from fastapi.datastructures import Default
from fastapi.encoders import SetIntStr, DictIntStrAny
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute

from .network import make_request
from .utils.body import unzip_body_object
from .utils.form import unzip_form_params
from .utils.query import unzip_query_params
from .utils.request import create_request_data
from .utils.headers import (
    inheritance_service_headers,
    generate_headers_for_microservice,
)


def route(
    request_method,
    gateway_path: str,
    service_url: str,
    service_path: Optional[str] = None,
    query_params: Optional[List[str]] = None,
    form_params: Optional[List[str]] = None,
    body_params: Optional[List[str]] = None,
    override_headers: bool = True,
    response_model: Optional[Type[Any]] = None,
    status_code: Optional[int] = None,
    tags: Optional[List[str]] = None,
    dependencies: Optional[Sequence[params.Depends]] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    response_description: str = "Successful Response",
    responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
    deprecated: Optional[bool] = None,
    operation_id: Optional[str] = None,
    response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    include_in_schema: bool = True,
    response_class: Type[Response] = Default(JSONResponse),
    name: Optional[str] = None,
    callbacks: Optional[List[BaseRoute]] = None,
    openapi_extra: Optional[Dict[str, Any]] = None,
    timeout: int = 60,
):
    """

    :param gateway_path: is the path to bind gateway.
    :param service_path: the path to the endpoint on another service.
    :param request_method: is a callable (like app.get, app.post and so on.)
    :param service_url: is url path to microservice (like "https://api.example.com/v1")
    :param query_params: used to extract query parameters from endpoint and transmission to microservice
    :param form_params: used to extract form model parameters from endpoint and transmission to microservice
    :param body_params: used to extract body model from endpoint and transmission to microservice
    :param override_headers: returns the original microservice headlines
    :param response_model: shows return type and details on api docs
    :param status_code: expected HTTP(status.HTTP_200_OK) status code
    :param tags: Allows grouped objects in the api docs
    :param dependencies: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/dependencies/#declare-the-dependency-in-the-dependant
    :param summary: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#summary-and-description
    :param description: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#summary-and-description
    :param response_description: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#response-description
    :param responses: See documentation for details -
        https://fastapi.tiangolo.com/advanced/additional-responses/
    :param deprecated: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/path-operation-configuration/#deprecate-a-path-operation
    :param operation_id: See documentation for details -
        https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
    :param response_model_include: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude
    :param response_model_exclude: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude
    :param response_model_by_alias: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/response-model/#response_model_include-and-response_model_exclude
    :param response_model_exclude_unset: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter
    :param response_model_exclude_defaults: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter
    :param response_model_exclude_none: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/response-model/#use-the-response_model_exclude_unset-parameter
    :param include_in_schema: See documentation for details -
        https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/#exclude-from-openapi
    :param response_class: See documentation for details -
        https://fastapi.tiangolo.com/advanced/custom-response/
    :param name: See documentation for details -
        https://fastapi.tiangolo.com/tutorial/metadata/
    :param callbacks: See documentation for details -
        https://fastapi.tiangolo.com/advanced/openapi-callbacks/
    :param openapi_extra: See documentation for details -
        https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/

    :return: wrapped endpoint result as is
    """

    register_endpoint = request_method(
        path=gateway_path,
        response_model=response_model,
        status_code=status_code,
        tags=tags,
        dependencies=dependencies,
        summary=summary,
        description=description,
        response_description=response_description,
        responses=responses,
        deprecated=deprecated,
        operation_id=operation_id,
        response_model_include=response_model_include,
        response_model_exclude=response_model_exclude,
        response_model_by_alias=response_model_by_alias,
        response_model_exclude_unset=response_model_exclude_unset,
        response_model_exclude_defaults=response_model_exclude_defaults,
        response_model_exclude_none=response_model_exclude_none,
        include_in_schema=include_in_schema,
        response_class=response_class,
        name=name,
        callbacks=callbacks,
        openapi_extra=openapi_extra,
    )

    def wrapper(f):
        @register_endpoint
        @functools.wraps(f)
        async def inner(request: Request, response: Response, **kwargs):
            scope = request.scope
            scope_method = scope["method"].lower()
            content_type = str(request.headers.get('Content-Type'))
            request_form = (
                await request.form() if 'x-www-form-urlencoded' in content_type else None
            )

            prepare_microservice_path = f"{service_url}{gateway_path}"
            if service_path:
                prepare_microservice_path = f"{service_url}{service_path}"

            microservice_url = prepare_microservice_path.format(**scope["path_params"])
            request_body = await unzip_body_object(
                necessary_params=body_params,
                all_params=kwargs,

            )

            request_query = await unzip_query_params(
                necessary_params=query_params, all_params=kwargs
            )
            request_form = await unzip_form_params(
                necessary_params=form_params,
                request_form=request_form,
                all_params=kwargs,
            )

            request_headers = generate_headers_for_microservice(
                headers=request.headers,
            )

            request_data = create_request_data(
                form=request_form,
                body=request_body,
            )

            try:
                (
                    resp_data,
                    status_code_from_service,
                    microservice_headers,
                ) = await make_request(
                    url=microservice_url,
                    method=scope_method,
                    data=request_data,
                    query=request_query,
                    headers=request_headers,
                    timeout=timeout,
                )

            except ClientConnectorError:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Service is unavailable.",
                )
            except ContentTypeError:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Service error.",
                )

            if override_headers:
                service_headers = inheritance_service_headers(
                    gateway_headers=response.headers,
                    service_headers=microservice_headers,
                )

                response.headers.update(service_headers)
            response.status_code = status_code_from_service

            return resp_data

    return wrapper
