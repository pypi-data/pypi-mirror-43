from setuptools import setup

setup(
    name='windb',
    version='0.0.2',
    author='fuchen',
    author_email='ink.pad@163.com',
    url='https://github.com/fuchen/windb',
    description=u'Wind + MongoDb',
    packages=['windb'],
    install_requires=[
        'loguru',
        'pdwind',
        'pymongo'
    ],
    entry_points={
    }
)
