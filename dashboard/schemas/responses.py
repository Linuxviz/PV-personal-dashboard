from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
            }
        }
