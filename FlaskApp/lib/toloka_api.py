import requests

from lib.common import get_toloka_token
from lib.models import TolokaProject, PoolStatus, TolokaPool

TOLOKA_TOKEN = "AgAAAAA1yGA2AACtpZulzHbCHE2ynzRYeIJg7bI"  # get_toloka_token()


def simple_toloka_get_request(url):
    resp = requests.get(url,
                        timeout=7200.0,
                        headers={'Content-Type': 'application/json',
                                 'Authorization': f'OAuth {TOLOKA_TOKEN}'})

    return resp.json()


def parse_projects(projects):
    return [TolokaProject.from_json(project_json) for project_json in projects]


def parse_pools(pools):
    return [TolokaPool(pools_json) for pools_json in pools]


def list_projects():
    url = f'https://toloka.yandex.ru/api/v1/projects?status=ACTIVE&limit=300&sort=id'
    projects = simple_toloka_get_request(url)['items']

    return parse_projects(projects)


def get_pool_tasks(pool_id):
    url = f'https://toloka.yandex.com/api/v1/assignments?pool_id={pool_id}&status=ACCEPTED,REJECTED&limit=10000'

    return simple_toloka_get_request(url)['items']


def count_pool_stats(pool_id):
    tasks = get_pool_tasks(pool_id)
    return len(list(filter(lambda t: t['status'] == "ACCEPTED", tasks))), \
           len(list(filter(lambda t: t['status'] == "REJECTED", tasks)))


def get_pools(project_id, status: PoolStatus):
    url = f'https://toloka.yandex.com/api/v1/pools?project_id={project_id}&status={status.value}'

    return parse_pools(simple_toloka_get_request(url)['items'])


if __name__ == "__main__":
    a = get_pool_tasks('27324585')
    print(a)
