from beanie import Document
from pydantic.color import Color


class Tag(Document):
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
