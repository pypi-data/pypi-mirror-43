import io

from setuptools import setup, find_packages

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='type-checker',
    version='1.0.1',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    author='Robert Parker',
    author_email='rob@parob.com',
    url='https://gitlab.com/robjampar/type-checker',
    download_url='https://gitlab.com/robjampar/type-checker/-/archive/v1.0.1/type-checker-v1.0.1.tar.gz',
    keywords=['Type', 'Checker', 'Validator'],
    description='Type checker helpers for Python.',
    long_description=readme,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
