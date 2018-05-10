# Elastic Search Helper
This package is inteded to be used to log feature usage and track utilization of different features of the software.


# install
```
pip install elasticsearch_helper
```

# usage

```python
helper = ElasticSearchHelper.get_instance(host='INDEX_HOST_NAME', index='test_index')
helper.log_feature('test_elasticsearch_factory_0')
```