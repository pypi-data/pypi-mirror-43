from setuptools import setup
from pip._internal.req import parse_requirements
import subprocess

install_reqs = parse_requirements('requirements.txt', session='hack')
requires = [str(ir.req) for ir in install_reqs]
lamblackbox_version_bytes = subprocess.run(
    ['git', 'describe', '--tags', '--abbrev=0'], stdout=subprocess.PIPE).stdout.decode('utf-8')

setup(
    name='lamblackbox',
    version=lamblackbox_version_bytes,
    description='This is a AWS Lambda function logging library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/youyo/lamblackbox',
    author='youyo',
    author_email='1003ni2@gmail.com',
    install_requires=requires,
    license="MIT License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='aws lambda log logger logging',
    packages=['lamblackbox'],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/youyo/lamblackbox',
    },
)
