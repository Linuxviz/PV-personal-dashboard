from pydantic import BaseModel


class Column(BaseModel):
    """
    """
    name: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'Column 1',
            }
        }

