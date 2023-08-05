from setuptools import setup

setup(
    name='bitbucket-pipes-toolkit',
    version='0.1.0',
    packages=['bitbucket_pipes_toolkit', ],
    url='https://bitbucket.org/bitbucketpipelines/pipes-tools-python/src',
    author='Atlassian',
    author_email='bitbucketci-team@atlassian.com',
    description='This package containes various helpers for developing bitbucket pipelines pipes',
    long_description=open('README.md').read()
)
