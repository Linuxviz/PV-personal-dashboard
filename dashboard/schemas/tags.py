from typing import List, Optional

import uuid as uuid
from pydantic import BaseModel
from pydantic.color import Color

from dashboard.schemas.responses import Response


class Tag(BaseModel):
    """
    Color properties:

        * name (e.g. "Black", "azure")

        * hexadecimal value (e.g. "0x000", "#FFFFFF", "7fffd4")

        * RGB/RGBA tuples in **JSON** (e.g. [255, 255, 255], [255, 255, 255, 0.5])

        * RGB/RGBA strings (e.g. "rgb(255, 255, 255)", "rgba(255, 255, 255, 0.5)")

        * HSL strings (e.g. "hsl(270, 60%, 70%)", "hsl(270, 60%, 70%, .5)")

    """
    id: Optional[uuid.UUID] = uuid.uuid4()
    name: str
    color: Color

    class Config:
        schema_extra = {
            "example": {
                'name': 'tag_name',
                'color': 'red'
            }
        }


class TagUpdate(BaseModel):
    name: Optional[str]
    color: Optional[Color]

    #TODO name or color must be
    # @root_validator
    # def check_passwords_match(cls, values):
    #     pw1, pw2 = values.get('password1'), values.get('password2')
    #     if pw1 is not None and pw2 is not None and pw1 != pw2:
    #         raise ValueError('passwords do not match')
    #     return values

    class Config:
        schema_extra = {
            "example1": {
                'name': 'tag_name',
                'color': 'red'
            },
            "example2": {
            },
            "example3": {
                'color': 'white'
            },
            "example4": {
                'name': 'new_name_for_tag',
            },
        }


class TagListResponse(Response):
    tags: List[Tag]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "tags": [Tag.Config.schema_extra, ]
            }
        }


class TagChangeResponse(Response):
    tag: Tag

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "tag": Tag.Config.schema_extra
            }
        }
