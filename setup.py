from setuptools import setup

setup(
    name='msu_pong_game',
    packages=['client'],
    entry_points = {
        'console_scripts': ['pong_game=client.__main__:main'],
    }
)