# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A setup module for the Google Ads API client library."""

from setuptools import setup, find_packages
import io

install_requires = [
    'enum34; python_version < "3.4"',
    'google-auth-oauthlib >= 0.0.1, < 1.0.0',
    'google-api-core == 1.7.0',
    'grpcio == 1.18.0',
    'PyYAML >= 4.2b1, < 5.0',
]

tests_require = [
    'mock >= 2.0.0, < 3.0.0',
    'pyfakefs >= 3.4, < 3.5',
]

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

setup(
    name='google-ads',
    version='1.0.0',
    author='Google LLC',
    author_email='googleapis-packages@google.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description='Client library for the Google Ads API',
    include_package_data=True,
    long_description=long_description,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite='tests',
    license='Apache 2.0',
    packages=find_packages(exclude=['examples', 'examples.*', 'tests', 'tests.*']),
    namespace_packages=['google', 'google.ads'],
    url='https://github.com/googleads/google-ads-python',
    zip_safe=False,
)
