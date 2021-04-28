from setuptools import setup

version = open('client/VERSION').read()
requirements = open('requirements.txt').read().splitlines()

setup(
    name='csmsu2020_pong_game',
    packages=['client', 'common'],
    package_data={'': [
        'localization/en_US/LC_MESSAGES/messages.mo',
        'localization/ru_RU/LC_MESSAGES/messages.mo'
    ]},
    include_package_data=True,
    install_requires=requirements,
    version=version,
    entry_points={
        'console_scripts': ['csmsu2020_pong_game=client.__main__:main'],
    }
)
