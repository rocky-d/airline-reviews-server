import json
from typing import Iterable

from redis import Redis, ConnectionPool


def get_rp() -> ConnectionPool | None:
    redis_pool: ConnectionPool | None = None
    try:
        redis_pool = ConnectionPool(
            host = '192.168.0.115',
            port = 6379,
            db = 1)
        print('Redis database connected!')
    except Exception as e:
        print(e)
    finally:
        return redis_pool


def iter_redis_list(redis_client: Redis, list_key: str) -> Iterable[str]:
    for index in range(redis_client.llen(list_key)):
        yield redis_client.lindex(list_key, index)


def update_redis_list(redis_client: Redis, list_key: str, new_list: list[str]) -> None:
    redis_client.delete(list_key)
    for row in new_list:
        redis_client.rpush(list_key, row)


def get_reviews_for_airline(redis_client: Redis, airl_name: str) -> str | None:
    for arl_json in iter_redis_list(redis_client, 'AIRLINE'):
        arl_dict = json.loads(arl_json)
        if airl_name == arl_dict['ARL_NAME']:
            airl_iata = arl_dict['ARL_IATA']
            break
    else:
        return None
    res = ''
    for rev_json in iter_redis_list(redis_client, 'REVIEW'):
        rev_dict = json.loads(rev_json)
        if airl_iata == rev_dict['REV_FLT_TAG']['REV_FLT_ARL_IATA']:
            res += rev_dict['REV_TITLE'] + rev_dict['REV_CONTENT']
    return (res
            .strip()
            .lower()
            .replace('\'', ' ')
            .replace('.', ' ')
            .replace(',', ' ')
            .replace(':', ' ')
            .replace(';', ' '))
