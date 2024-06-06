from setuptools import setup, find_packages

setup(
    name='covid_tweets',
    version='1.0',
    packages=find_packages('src', 'tests'),
    package_dir={'': 'src', 'tests': 'tests'},
    install_requires=[
        'apache-beam==2.56.0',
        'beautifulsoup4==4.12.3',
        'pymongo==4.7.2',
        'requests==2.32.3',
        'pytest',
        'mock'
    ],
    test_suite='tests',
    tests_require=['pytest'],
    python_requires='==3.9.19',
)
