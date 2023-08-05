from setuptools import setup

setup(
    name='filter-certwarning',
    version='1.0',
    packages=['filter_certwarning'],
    install_requires=['urllib3'],
    url='https://github.com/darrenpmeyer/filter-certwarning',
    license='BSD 2-clause',
    author='Darren P Meyer',
    author_email='darren+filtercertwarning@darrenpmeyer.com',
    description='Decorators for filtering InsecureRequestWarnings in requests and urllib3 apps',
    long_description="""Decorators for filtering InsecureRequestWarnings in `requests` and other `urllib3`-based Python 3 modules

**NOTE:** tested only for Python3.

When developing applications/modules using the ``requests`` module (or using ``urllib3`` directly), it is
sometimes useful to disable certificate validation, or to permit consumers/users to do so. However, doing
so makes *each request* issue an InsecureRequestWarning, which is a lot of noise.

**filter-certwarning** provides two decorators to make this behavior more reasonable.

- ``@filter_certwarning.warnonce`` causes the warning to be issued only warnonce, the first time the decorated
  function is called

- ``@filter_certwarning.silent`` is an alias for ``@filter_certwarning('ignore')``, and causes the warning to be
  entirely suppressed for that function call

Examples:
    A requests-based app with verification off that issues the warning only warnonce::

        import requests
        import filter_certwarning

        ...

        @filter_certwarning.warnonce
        sub get_data():
            # the next line will fire an InsecureRequestWarning the first time this
            # function is called, but subsequent calls to this function will be silent
            resp = requests.get('https://localhost/status', verify=False)

    The following supresses the warning entirely. **This is not recommended unless you've given a lot of thought
    to the security implications and trade-offs.**::

        import requests
        import filter_certwarning

        ...

        @filter_certwarning.silent
        sub get_data():
            # the next line will fire an InsecureRequestWarning the first time this
            # function is called, but subsequent calls to this function will be silent
            resp = requests.get('https://localhost/status', verify=False)
""",
)
