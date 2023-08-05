
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

import os
import json
import setuptools

import setupextras


# =========================================
#       PACKAGE
# --------------------------------------

name = 'foo'
version = '1.0.0'
description = 'A foo library.'
keywords = [
    'foo',
    'bar',
]

packages = setupextras.get_packages()
data_files = setupextras.get_data_files(['*.*'], os.path.join(name, 'tests', '__fixtures__'))
requirements = setupextras.get_requirements()
readme = setupextras.get_readme()

config = {
    'name': name,
    'version': version,
    'description': (description),
    'keywords': keywords,
    'author': 'Jonas Grimfelt',
    'author_email': 'grimen@gmail.com',
    'url': 'https://github.com/grimen/python-{name}'.format(name = name),
    'download_url': 'https://github.com/grimen/python-{name}'.format(name = name),
    'project_urls': {
        'repository': 'https://github.com/grimen/python-{name}'.format(name = name),
        'bugs': 'https://github.com/grimen/python-{name}/issues'.format(name = name),
    },
    'license': 'MIT',
    'long_description': readme,
    'packages': packages,
    'data_files': data_files,
    'install_requires': requirements,
}

print('CONFIG {0}'.format(json.dumps(config, indent = 4)))


# =========================================
#       MAIN
# --------------------------------------

setuptools.setup(**config)
