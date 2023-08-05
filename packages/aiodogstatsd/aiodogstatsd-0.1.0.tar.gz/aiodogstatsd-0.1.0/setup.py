# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiodogstatsd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiodogstatsd',
    'version': '0.1.0',
    'description': 'An asyncio-based client for sending metrics to StatsD with support of DogStatsD extension',
    'long_description': '# aiodogstatsd\n\nAn asyncio-based client for sending metrics to StatsD with support of [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/) extension.\n\nLibrary fully tested with [statsd_exporter](https://github.com/prometheus/statsd_exporter) and supports `gauge`, `counter`, `histogram`, `distribution` and `timing` types.\n\n## Installation\n\n```sh\n$ pip install aiodogstatsd\n```\n\n## Usage\n\n```python\nimport asyncio\n\nimport aiodogstatsd\n\n\nasync def main():\n    client = aiodogstatsd.Client()\n    await client.connect()\n\n    client.increment("users.online")\n\n    await client.close()\n\n\nasyncio.run(main())\n```\n\nLook at `examples/` to find more examples of library usage.\n\n## Contributing\n\nTo work on the `aiodogstatsd` codebase, you\'ll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:Gr1N/aiodogstatsd.git\n$ poetry install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ poetry run tox\n```\n\nIf you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:\n\n```sh\n$ poetry run tox -e py37-tests\n```\n\n## License\n\n`aiodogstatsd` is licensed under the MIT license. See the license file for details.\n',
    'author': 'Nikita Grishko',
    'author_email': 'gr1n@protonmail.com',
    'url': 'https://github.com/Gr1N/aiodogstatsd',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
