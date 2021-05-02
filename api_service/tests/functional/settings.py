from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field("http://127.0.0.1:9200", env="ELASTIC_HOST")
    api_base_url: str = Field("http://127.0.0.1:8000/api/v1", env="BASE_API_URL")
