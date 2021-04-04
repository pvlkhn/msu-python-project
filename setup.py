from setuptools import setup

version = open('client/VERSION').read()

setup(
    name='csmsu2020_pong_game',
    packages=['client'],
    version=version,
    entry_points = {
        'console_scripts': ['pong_game=client.__main__:main'],
    }
)