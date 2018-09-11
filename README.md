# django-scooby-profiler

This is a developer tool package to debug Django applications.
The aim of this package is more or less same as of Django debug toolbar,
but I made it because of these shortcomings of django-debug-toolbar package:

1) You can not debug AJAX requests with django-debug-toolbar.
2) If you have a big Django project, the django-debug-toolbar makes web pages more slower
because it injects its own html by rendering which takes time.

## With django-scooby-profiler:

1) You can debug AJAX requests as well.
2) It comes with a chrome extension named "Scooby profiler", so rendering happens at front-end only.
3) You have to switch on debugging in chrome extension, only then backend will collect profiled data for all queries.
This way, the overhead caused by debugging is not always ON by default.

Here's how the issues are mitigated in django-scooby-profiler.
All the profiled data collected is dumped to a backend (E.g. Redis) where the data resides temporarily.
The chrome extension collects those data and renders it to you for different HTTP requests.

## Plugins supported
Currently plugins for these type of queries are supported by this package:

1) **SQL**:
Debug SQL queries happening inside the app, while serving a request. It shows all SQL queries with proper stacktrace.
You can group together similar queries at front-end, so that you would know what queries you can optimize.
This is what generally happens in case of `for` loops.

2) **Memcache**:
It shows different operations on memcache with stacktraces.

3) **Scooby logs**:
Instead of debugging/printing on console, you can log things directly to extension.
Do it by putting following anywhere in you code where you want to log.

```python
import scooby
scooby.log("foo", "bar")
# or
scooby.log()         # It works without giving any argument too.
```

4) **Python cProfile**:
If you want to use raw python profiler on your Django view, you don't need to add any extra code for that.
This plugin does the job for you.

If you don't find a plugin here which you think should be here, you are most welcome to contribute it to this package.

## Installation

```bash
# Use pip in case of Python 2
pip3 install django-scooby-profiler 
```

## Backend configuration

1) Add 'scooby' to `INSTALLED_APPS` setting.
```python
INSTALLED_APPS = [
  ...,
  'scooby',
]
```

2) Add this middeware to `MIDDLEWARE_CLASSES` setting (usage with new style middlewares is not supported yet):
```python
MIDDLEWARE_CLASSES = [
  'scooby.middleware.ScoobyMiddleware',
  ...,
]
```

3) Add following manadatory settings:

* **SCOOBY_SECRET_KEY** (type: string)

You can generate a secret key by
```
>>> import os
>>> import binascii
>>> print(binascii.hexlify(os.urandom(24)))
0ccd512f8c3493797a23557c32db38e7d51ed74f14fa758
```


* **SCOOBY_REDIS_BACKEND_CONFIG** (type: dict, connection params required for redis connection)

This is not required if SCOOBY_BACKEND is set as some other backend.
The setting would look like

```python
SCOOBY_REDIS_BACKEND_CONFIG = {
  'host': 'localhost',
  'port': 6379
}
```

4) Add scooby base url to your project's urlconf by

```
urlpatterns = [
    ...,
    url(r'^scooby/', include('scooby.urls')),
]
```

### Other optional Settings

* **SCOOBY_DEBUG** (type: boolean, default: DEBUG)
Whether to debug or not regarding this package.

* **SCOOBY_BACKEND** (type: string, path to the class which acts as backend, default: 'scooby.backends.RedisBackend')
You can specify your own backend if you don't want to use Redis.
You need to create a class similar to `RedisBackend` defined in `scooby/backends.py`


## Install chrome extension
Install the chrome extension from https://chrome.google.com/webstore/detail/scooby-profiler/kicgfdanpohconjegfkojbpceodecjad

Open the developer tools in your browser, you will see a section named "Scooby".
It will ask for the secret key, which you need to put as same you have put in the backend.
Reload your page, you will start seeing HTTP requests with profiled data for all supported plugins.

## LICENCE
MIT
