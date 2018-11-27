from setuptools import setup, find_packages

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
        long_description = f.read()

# setup the project
setup(
    name="django-scooby-profiler",
    version="2.0.5",
    url="https://github.com/shhaumb/django-scooby-profiler",
    author="Shubham Jain",
    author_email="sj.iitr@gmail.com",
    description=(
        "A debugging tool for Django applications which works for all HTTP "
        "requests including AJAX. Using this, you can profile Django views. "
        "It shows you all SQL, Memcache queries with proper stacktrace "
        "happening in app while serving a request, with the help of "
        "'Scooby profiler' chrome extension."
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="django debugging profiler profiling sql tool",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'redis',
        'pyjwt',
    ]
)
