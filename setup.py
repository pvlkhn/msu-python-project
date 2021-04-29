from setuptools import setup

version = open('VERSION').read()
requirements = open('requirements.txt').read().splitlines()

setup(
    name='csmsu2020_pong_game',
    packages=['client', 'common', 'server'],
    package_data={'': [
        'localization/en_US/LC_MESSAGES/messages.mo',
        'localization/ru_RU/LC_MESSAGES/messages.mo'
    ]},
    include_package_data=True,
    install_requires=requirements,
    version=version,
    url='https:///github.com/pvlkhn/msu-python-project',
    entry_points={
        'console_scripts': [
            'csmsu2020_pong_game=client.__main__:main',
            'csmsu2020_pong_server=server.__main__:main'
        ],
    }
)
