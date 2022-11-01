from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from aiohttp import FormData
from starlette.datastructures import FormData as FormDataStarlette
from starlette.datastructures import UploadFile


class CustomFormDataStorage(FormData):
    def add_www_form(self, name: str, value: Any):
        self.add_field(name=name, value=value)

    def add_multipart_form(
        self,
        name: str,
        filename: Optional[str],
        value: Any,
        content_type: Optional[str] = None,
    ):
        self.add_field(
            name=name, filename=filename, value=value, content_type=content_type
        )


class CustomFormData(CustomFormDataStorage):
    async def upload(self, key, value: Union[UploadFile, str]):
        if isinstance(value, UploadFile):
            bytes_file = await value.read()
            self.add_multipart_form(
                name=key,
                filename=value.filename,
                value=bytes_file,
                content_type=value.content_type,
            )
        elif isinstance(value, str):
            self.add_www_form(name=key, value=value)


async def unzip_form_params(
    all_params: Dict[str, Any],
    necessary_params: Optional[List[str]] = None,
    request_form: Optional[FormDataStarlette] = None,
) -> Optional[CustomFormData]:
    if necessary_params or request_form:
        body_form = CustomFormData()
        if necessary_params:
            for key in necessary_params:
                value = all_params.get(key)
                await body_form.upload(key=key, value=value)

        if request_form:
            for key in request_form:
                await body_form.upload(key=key, value=request_form[key])
        return body_form
    return None
