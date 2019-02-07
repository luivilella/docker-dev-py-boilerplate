import os

import bottle
import psycopg2


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


@bottle.route('/')
def index():
    active_users = get_db_active_users()
    return f'Active users: {active_users}'


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=8080)
