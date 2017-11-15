from setuptools import setup, find_packages

# setup the project
setup(
    name="scooby-django",
    version="1.0.1",
    author="HackerEarth",
    author_email="support@hackerearth.com",
    description="Scooby",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'redis==2.10.6',
    ]
)
