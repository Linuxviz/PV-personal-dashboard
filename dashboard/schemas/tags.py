from typing import List

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
    name: str
    color: Color

    class Config:
        schema_extra = {
            "example": {
                'name': 'tag_name',
                'color': 'Color'
            }
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


class TagCreateResponse(Response):
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
