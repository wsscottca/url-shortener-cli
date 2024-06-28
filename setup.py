''' Module included the setup build specs '''
from setuptools import setup, find_packages

setup(
    name='url-shortener-cli',
    version='1.0',
    author='wsscottca',
    description='Command Line Interface for FastAPI URL shortener',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['url-shortener=app.main:cli'],
    },
    install_requires=[
        'pydantic>=2.6.2',
        'click>=8.1.7',
        'requests>=2.31.0',
        'responses>=0.25.0',
        'python-dotenv>=1.0.1'
    ],
    package_data={
        'app': ['*.env'],
    },
    include_package_data=True
)
