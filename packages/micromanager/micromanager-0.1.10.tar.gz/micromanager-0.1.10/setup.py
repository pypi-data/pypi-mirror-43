from __future__ import print_function

from setuptools import setup

setup(
    name="micromanager",
    description="Policy enforcement tool for GCP",
    long_description='Tool to load resources from GCP, check them against policies written in Rego, and attempt remediation of policy violations.',
    author="Joe Ceresini",
    url="https://github.com/cleardataeng/micromanager",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'google-api-python-client',
        'google-api-python-client-helpers',
        'tenacity',
    ],
    packages=[
        'micromanager',
        'micromanager.engines',
        'micromanager.resources',
    ],
    package_data={},
    license="Apache 2.0",
    keywords="gcp policy enforcement",
)

