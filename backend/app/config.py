from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_url: str = "Add your MongoDB URL here"
    database_name: str = "Add your database name here"
    max_connection_pool_size: int = 10
    min_connection_pool_size: int = 10


settings = Settings()
