from functools import lru_cache
from http import HTTPStatus

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, HTTPException

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.base import Service


class PersonService(Service):
    es_index = "persons"
    model_type = Person

    async def search_persons(
        self, url: str, query: str, page_number: int, page_size: int
    ) -> list[Person]:

        query = {"multi_match": {"query": query, "fields": ["first_name", "last_name"]}}

        body = {
            "from": page_number * page_size,
            "size": page_size,
            "query": query,
        }

        return await self._search(url, body=body)


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
