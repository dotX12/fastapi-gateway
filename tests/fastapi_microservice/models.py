from pydantic import BaseModel


class ExampleModel(BaseModel):
    example_int: int
    example_str: str
