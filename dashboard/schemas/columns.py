import uuid

from pydantic import BaseModel


class Column(BaseModel):
    """
    """
    id: uuid.UUID
    name: str

    class Config:
        schema_extra = {
            "example": {
                'id': 'c45df5a6-8ffc-4c7f-9eb7-7931def164f3',
                'name': 'Column 1',
            }
        }


class ColumnCreate(BaseModel):
    """
    """
    name: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'Column 1',
            }
        }


class ColumnUpdate(BaseModel):
    """
    """
    name: str

    class Config:
        schema_extra = {
            "example": {
                'name': 'New Column',
            }
        }
