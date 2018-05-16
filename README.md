# Elastic Search Helper
This package is inteded to be used to log feature usage and track utilization of different features of python code and push it to elasticsearch.

By default, a new thread will be created that will push data to elasticsearch every 10 seconds.

This package doesn't make use of python logging. If you prefer to use python logging, use CMRESHandler, which has more features and better error handling
https://github.com/cmanaha/python-elasticsearch-logger

In some cases, where python logging is globally disabled, this package will still work.

# How to install
```
pip install elasticsearch_util
```
if you are behind proxy

```
set http_proxy=http://<YOUR_PROXY_HOST>:<YOUR_PROXY_PORT>
set https_proxy=http://<YOUR_PROXY_HOST>:<YOUR_PROXY_PORT>
pip install elasticsearch_util
```

# Basic usage
Here is a simple way to use this library.

```python
from elasticsearch_util.helper import ElasticSearchHelper
helper = ElasticSearchHelper.get_instance(host='INDEX_HOST_NAME', index='test_index')
helper.log_feature('test_my_feature')
```

# Advanced usage
You can use this library as a decorator to make it easy to track specific function usage. Decorator will automatically track:
- Exception information (traceback)
- Execution duration

Decorator will not alter function behavior and will return. This will add an overhead to the function and shouldn't be used in recursive functions or in a function that is invoked excessively.

```python
from elasticsearch_util.helper import ElasticSearchHelper
helper = ElasticSearchHelper.get_instance(host='INDEX_HOST_NAME', index='test_index')

@helper.log_feature_decorator("func_to_decorate_executed", developer="gehad")
def func_to_decorate():
    pass

# calling function will add record to buffer which will be flushed periodically if auto_flush is enabled
func_to_decorate()
```
Check test_all.py for more examples.

# Release
To make a release you will need to be a collaborator on the porject. Please contact package owner to be added as a collaborator.

It will ask for username and password
```
pip install twine
python setup.py sdist
twine upload dist/*
```

# Test
To run unittest, install pytest first. It currently assumes server is at port 9200 for server
test will actually push data to test_index
```
pip install pytest
set ELASTIC_SEARCH_HOST=elasticsearch-server
python - m pytest test_all.py

```
