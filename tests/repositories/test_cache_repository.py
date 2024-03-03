import json
from random import randint
from unittest.mock import patch

from app.core.config import setting

CACHE_KEY = "repo:somone:somrepo"


def generate_random_star_count_and_forks_count():
    return randint(0, 1000), randint(0, 1000)


def generate_external_git_info_and_set_into_cache(redis_repo, stargazers_count, forks_count):
    data = {
        "stargazers_count": stargazers_count,
        "forks_count": forks_count
    }

    return redis_repo.set(CACHE_KEY, json.dumps(data), ttl=setting.CACHE_DATA_TIME_TO_LIVE)


def test_cache_repo_can_set_and_get_data_into_redis_successfully(client, container, redis):
    stargazers_count, forks_count = generate_random_star_count_and_forks_count()
    redis_repo = container.redis_repository()

    cache_data_from_redis = redis_repo.get(CACHE_KEY)
    assert not cache_data_from_redis

    generate_external_git_info_and_set_into_cache(redis_repo, stargazers_count, forks_count)

    cache_data_from_redis = json.loads(redis_repo.get(CACHE_KEY))
    assert cache_data_from_redis['stargazers_count'] == stargazers_count
    assert cache_data_from_redis['forks_count'] == forks_count


def test_get_non_existent_key_returns_none(client, container, redis):
    redis_repo = container.redis_repository()
    result = redis_repo.get(CACHE_KEY)
    assert result is None


def test_cache_repo_can_update_data_in_redis_successfully(client, container, redis):
    initial_stargazers_count, initial_forks_count = generate_random_star_count_and_forks_count()

    redis_repo = container.redis_repository()

    cache_data_from_redis = redis_repo.get(CACHE_KEY)
    assert not cache_data_from_redis

    generate_external_git_info_and_set_into_cache(redis_repo, initial_stargazers_count, initial_forks_count)
    cache_data_from_redis = json.loads(redis_repo.get(CACHE_KEY))

    assert cache_data_from_redis['stargazers_count'] == initial_stargazers_count, "Stargazers count was not created"
    assert cache_data_from_redis['forks_count'] == initial_forks_count, "Forks count was not created"

    updated_stargazers_count, updated_forks_count = generate_random_star_count_and_forks_count()

    generate_external_git_info_and_set_into_cache(redis_repo, updated_stargazers_count, updated_forks_count)
    cache_data_from_redis = json.loads(redis_repo.get(CACHE_KEY))

    assert cache_data_from_redis[
               'stargazers_count'] == updated_stargazers_count, "Stargazers count was not updated correctly"
    assert cache_data_from_redis['forks_count'] == updated_forks_count, "Forks count was not updated correctly"
    assert cache_data_from_redis != {
        "stargazers_count": initial_stargazers_count,
        "forks_count": initial_forks_count
    }, "Cache data should not match initial data after update"
