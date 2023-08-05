# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dramatiq_pg']

package_data = \
{'': ['*']}

install_requires = \
['dramatiq>=1.5,<2.0', 'psycopg2>=2.7,<3.0']

entry_points = \
{'console_scripts': ['dramatiq-pg = dramatiq_pg.cli:entrypoint']}

setup_kwargs = {
    'name': 'dramatiq-pg',
    'version': '0.3.0',
    'description': 'Postgres Broker for Dramatiq Task Queue',
    'long_description': '# dramatiq-pg − Postgres Broker for Dramatiq\n\n[dramatiq](https://dramatiq.io/) is a simple task queue implementation for\nPython3. dramatiq-pg provides a Postgres-based implementation of a dramatiq\nbroker.\n\n**The project is not feature complete yet.**\n\n## Features\n\n- Super simple deployment.\n- Uses plain psycopg2. No ORM.\n- Stores message payload as native JSONb.\n- Stores all messages in a single table, in a dedicated schema.\n- Uses LISTEN/NOTIFY to keep worker sync. No polling.\n- Replay pending messages on worker startup.\n- Requeues failed tasks.\n- Reliable thanks to Postgres MVCC.\n- Self-healing. Old messages are purge from time to time.\n\nNote that dramatiq assumes tasks are idempotent. This broker makes the same\nassumptions for recovering after a crash.\n\n\n## Installation\n\n- Install dramatiq-pg package from PyPI:\n  ``` console\n  $ pip install dramatiq-pg\n  ```\n- Apply dramatiq\\_pg/schema.sql file in your database:\n  ``` console\n  $ psql -f dramatiq_pg/schema.sql\n  ```\n- Before importing actors, define global broker with a connection\n  pool:\n  ``` python\n  import dramatiq\n  import dramatiq_pg\n  import psycopg2.pool\n\n  pool = psycopg2.pool.ThreadedConnectionPool(0, 4, conninfo)\n  dramatiq.set_broker(dramatiq_pg.PostgresBroker(pool=pool))\n  ```\n\nNow declare/import actors and manage worker just like any [dramatiq\nsetup](https://dramatiq.io/guide.html). An [example\nscript](https://gitlab.com/dalibo/dramatiq-pg/blob/master/example.py) is\navailable, tested on CI.\n\nThe CLI tool `dramatiq-pg` allows you to show stats on the queue and purge old\nmessages. See `--help` for details.\n\n\n## Roadmap\n\n- Result storage as JSONb.\n- Delayed task.\n\n\nFeel free to suggest feature through support channels.\n\n\n## Support\n\nIf you encounter a bug or miss a feature, please [open an issue on\nGitLab](https://gitlab.com/dalibo/dramatiq-pg/issues/new) with as much\ninformation as possible.\n\ndramatiq_pg is available under the PostgreSQL licence.\n',
    'author': 'Étienne BERSAC',
    'author_email': None,
    'url': 'https://gitlab.com/dalibo/dramatiq-pg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
