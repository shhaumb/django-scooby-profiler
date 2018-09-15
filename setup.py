from setuptools import setup, find_packages

# setup the project
setup(
    name="django-scooby-profiler",
    version="2.0.1",
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
    keywords="django debugging profiler profiling sql tool",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'redis',
        'pyjwt',
    ]
)
