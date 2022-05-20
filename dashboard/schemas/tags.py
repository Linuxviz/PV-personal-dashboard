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
        * RGB/RGBA tuples (e.g. (255, 255, 255), (255, 255, 255, 0.5))
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
                'color': 'Color'
            }
        }


class TagUpdate(BaseModel):
    name: Optional[str]
    color: Optional[Color]

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
