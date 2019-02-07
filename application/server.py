import os
from random import randint

import bottle
import psycopg2

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


cache_opts = {
    'cache.type': 'ext:redis',
    'cache.url': 'redis://redis-host/0'
}
cache = CacheManager(**parse_cache_config_options(cache_opts))


def get_db_active_users() -> list:
    """Function to get all active users from database

    Returns:
        list: list of strings with user's name

    Examples:
        >>> print(get_db_active_users())
        ['user1', 'user2']
    """

    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        host=os.getenv('DB_HOST'),
        password=os.getenv('DB_PASSWORD'),
    )

    cur = conn.cursor()
    sql = '''
        SELECT
            DISTINCT(usename) AS usename
        FROM pg_stat_activity
        WHERE
            state = 'active'
    '''
    cur.execute(sql)
    rows = cur.fetchall()
    return [usename for usename, in rows]


@cache.cache(expire=3)
def get_random(_min: int, _max: int) -> int:
    """This function is just a cached version of random.randint

    Returns:
        int: returns the sample result for 3 seconds
    """

    return randint(_min, _max)


@bottle.route('/')
def index():
    active_users = get_db_active_users()
    random_number = get_random(0, 1000)
    return f'Active users: {active_users} - random: {random_number}'


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080)
