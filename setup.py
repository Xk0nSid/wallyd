from setuptools import setup
from main import VERSION

setup(
    name='WallyDaemon',
    version=VERSION,
    py_modules=[
        "main",
    ],
    packages=[
        'wally',
    ],
    install_requires=[
        'Click',
        'toml',
    ],
    entry_points='''
    [console_scripts]
    wallyd=main:cli
    '''
)