from setuptools import setup, find_packages

setup(
    name='statcordAPI',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'discord.py',
        'aiohttp',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'mypackage=mypackage.__main__:main',
        ],
    },
)