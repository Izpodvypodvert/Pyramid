from pydantic import BaseModel


class OpenAPIDocExtraResponse(BaseModel):
    """Class for extra responses in OpenAPI doc"""

    detail: str
