from pydantic import Field
from pydantic_settings import BaseSettings


class GigachatConfig(BaseSettings):
    client_id: str = Field(validation_alias="GIGACHAT_CLIENT_ID")
    client_secret: str = Field(validation_alias="GIGACHAT_CLIENT_SECRET")
