
# =========================================
#       IMPORTS
# --------------------------------------

import rootpath

rootpath.append()

import setupextras

from setupextras.tests import helper

from os import path


# =========================================
#       TEST
# --------------------------------------

class TestCase(helper.TestCase):

    def test__import(self):
        self.assertModule(setupextras)

    def test_get_requirements(self):
        self.assertTrue(hasattr(setupextras, 'get_requirements'))
        self.assertTrue(callable(setupextras.get_requirements))

        result = setupextras.get_requirements()

        self.assertDeepEqual(result, [
            'six >= 1.11.0',
            'rootpath >= 0.1.1',
            'inspecta >= 0.1.0',
            'setuptools >= 40.8.0',
            'colour-runner >= 0.0.5',
            'deepdiff >= 3.3.0',
            'tox >= 3.0.0',
            'coverage >= 4.5.2',
            'codecov >= 2.0.15',
        ])

        foo_package_path = helper.fixture_path()

        result = setupextras.get_requirements(foo_package_path)

        self.assertDeepEqual(result, [])

        foo_package_path = helper.fixture_path('foo')

        result = setupextras.get_requirements(foo_package_path)

        self.assertDeepEqual(result, [])

    def test_get_packages(self):
        self.assertTrue(hasattr(setupextras, 'get_packages'))
        self.assertTrue(callable(setupextras.get_packages))

        result = setupextras.get_packages()

        self.assertDeepEqual(result, ['setupextras', 'setupextras.tests'])

        foo_package_path = helper.fixture_path()

        result = setupextras.get_packages(foo_package_path)

        self.assertDeepEqual(result, [])

        foo_package_path = helper.fixture_path('foo')

        result = setupextras.get_packages(foo_package_path)

        self.assertDeepEqual(result, [])

    def test_get_data_files(self):
        self.assertTrue(hasattr(setupextras, 'get_data_files'))
        self.assertTrue(callable(setupextras.get_data_files))

        result = setupextras.get_data_files()

        self.assertDeepEqual(result, [])

        foo_package_path = helper.fixture_path()

        result = setupextras.get_data_files()

        self.assertDeepEqual(result, [])

        foo_package_path = helper.fixture_path('foo')

        result = setupextras.get_data_files(foo_package_path)

        import json

        expected_result = list(map(lambda item: (
            (item[0].replace('<root>', helper.root_path()), item[1])
        ), [
            ('<root>', ['/']),
            ('<root>/setupextras', ['/']),
            ('<root>/setupextras/tests', ['/']),
            ('<root>/setupextras/tests/__fixtures__', ['/']),
            ('<root>/setupextras/tests/__fixtures__/py-foo', ['/']),
            ('<root>/setupextras/tests/__fixtures__/py-foo/bin', ['/']),
            ('<root>/setupextras/tests/__fixtures__/py-foo/foo', ['/']),
            ('<root>/setupextras/tests/__fixtures__/py-foo/foo/tests', ['/']),
            ('<root>/setupextras/tests/__fixtures__/py-foo/foo/tests/__fixtures__', ['/']),
            ('<root>/setupextras/tests/__fixtures__/py-foo/foo/tests/__fixtures__/foo', ['/']),
            ('<root>/examples', ['/']),
        ]))

        self.assertDeepEqual(result, expected_result)

    def test_get_readme(self):
        self.assertTrue(hasattr(setupextras, 'get_readme'))
        self.assertTrue(callable(setupextras.get_readme))

        result = setupextras.get_readme()

        with open(path.join(helper.root_path(), 'README.md')) as readme:
            self.assertDeepEqual(result, readme.read())

        foo_package_path = helper.fixture_path()

        result = setupextras.get_readme(foo_package_path)

        self.assertDeepEqual(result, None)

        foo_package_path = helper.fixture_path('py-foo')

        result = setupextras.get_readme(foo_package_path, silent = False)

        self.assertDeepEqual(result, '\n# foo\n\n*A foo library.*\n\n\n# Install\n\n```sh\npip install foo\n```\n\n# License\n\nReleased under the MIT license.\n')
