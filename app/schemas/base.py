from pydantic import (BaseModel, Extra)


class MyBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid
