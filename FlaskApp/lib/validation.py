from lib.models import TolokaPool, PoolStatus, TolokaProject
from lib.toloka_api import get_pool_tasks, count_pool_stats, get_pools


def track_pool(pool: TolokaPool, acceptance_rate: float):
    accepted, rejected = count_pool_stats(pool.id)

    if accepted == 0 or rejected == 0:
        return True

    return acceptance_rate >= accepted / (accepted + rejected)


def track_project(project: TolokaProject, max_pools_count: int):
    pools = get_pools(project.id, PoolStatus.OPEN)

    return max_pools_count <= len(pools)