import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'psycopg2',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_mako',
    ]

setup(name='alexandria',
      version='0.0',
      description='alexandria',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Bert JW Regeer',
      author_email='bertjw@regeer.org',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='alexandria',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = alexandria:main
      [console_scripts]
      alexandria_init_db = alexandria.scripts.initializedb:main
      alexandria_destroy_db = alexandria.scripts.destroydb:main
      """,
      )
