from pydantic import BaseModel


class ModelCheckPath(BaseModel):
    foo: str
    custom_int: str


class ModelCheckPathBody(ModelCheckPath):
    foo: str
    path_int: int
    example_int: int
    example_str: str


class FooModel(BaseModel):
    example_int: int
    example_str: str


class FooList(BaseModel):
    foo_key: str

