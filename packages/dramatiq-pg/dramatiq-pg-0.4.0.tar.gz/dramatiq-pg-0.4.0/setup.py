# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dramatiq_pg']

package_data = \
{'': ['*']}

install_requires = \
['dramatiq>=1.5,<2.0', 'psycopg2>=2.7,<3.0', 'pytest-mock>=1.10,<2.0']

entry_points = \
{'console_scripts': ['dramatiq-pg = dramatiq_pg.cli:entrypoint']}

setup_kwargs = {
    'name': 'dramatiq-pg',
    'version': '0.4.0',
    'description': 'Postgres Broker for Dramatiq Task Queue',
    'long_description': '# dramatiq-pg − Postgres Broker for Dramatiq\n\n[Dramatiq](https://dramatiq.io/) is a simple task queue implementation for\nPython3. dramatiq-pg provides a Postgres-based implementation of a dramatiq\nbroker.\n\n**The project is not feature complete yet.**\n\n## Features\n\n- Super simple deployment.\n- Uses plain psycopg2. No ORM.\n- Stores message payload as native JSONb.\n- Stores all messages in a single table, in a dedicated schema.\n- Uses LISTEN/NOTIFY to keep worker sync. No polling.\n- Replay pending messages on worker startup.\n- Requeues failed tasks.\n- Delayed task.\n- Reliable thanks to Postgres MVCC.\n- Self-healing. Old messages are purge from time to time.\n\nNote that dramatiq assumes tasks are idempotent. This broker makes the same\nassumptions for recovering after a crash.\n\n\n## Installation\n\n- Install dramatiq-pg package from PyPI:\n  ``` console\n  $ pip install dramatiq-pg\n  ```\n- Apply dramatiq\\_pg/schema.sql file in your database:\n  ``` console\n  $ psql -f dramatiq_pg/schema.sql\n  ```\n- Before importing actors, define global broker with a connection\n  pool:\n  ``` python\n  import dramatiq\n  import psycopg2.pool\n  from dramatiq_pg import PostgresBroker\n\n  dramatiq.set_broker(PostgresBroker(url="postgresql:///?minconn=0&maxconn=10"))\n\n  @dramatiq.actor\n  def myactor():\n      ...\n  ```\n\nNow declare/import actors and manage worker just like any [dramatiq\nsetup](https://dramatiq.io/guide.html). An [example\nscript](https://gitlab.com/dalibo/dramatiq-pg/blob/master/example.py) is\navailable, tested on CI.\n\nThe CLI tool `dramatiq-pg` allows you to requeue messages, purge old messages\nand show stats on the queue. See `--help` for details.\n\n\n## Deployment\n\nPostgres does not replicate notifications to standby instances. Thus the broker\nconnection pool must point to the master instance. Actor can connect to hot\nstandby for its work.\n\nIf you use pgbouncer, you must configure session pooling method to keep notify.\n\nEach dramatiq process opens one persistent connection per queue and one\nconnection to ack messages. Thus, to be save, you should provision pool size\nwith `num_processes x num_queues x 2`. A best practice is to only add process as\nneeded and reduce the number of queues.\n\n\n## Roadmap\n\n- Result storage as JSONb.\n\nFeel free to suggest feature through support channels.\n\n\n## Support\n\nIf you encounter a bug or miss a feature, please [open an issue on\nGitLab](https://gitlab.com/dalibo/dramatiq-pg/issues/new) with as much\ninformation as possible.\n\ndramatiq_pg is available under the PostgreSQL licence.\n',
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
