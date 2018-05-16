from pprint import pprint

import time
import os

import elasticsearch
from elasticsearch_util.helper import ElasticSearchHelper, MockElasticSearchHelper

# modify this to run tests
ELASTIC_SEARCH_HOST = os.environ['ELASTIC_SEARCH_HOST']


def test_elasticsearch_factory():
	helper = ElasticSearchHelper.get_instance(host=ELASTIC_SEARCH_HOST, index='test_index')
	helper.log_feature('test_elasticsearch_factory_0')
	helper.log_feature('test_elasticsearch_factory_1')
	time.sleep(1)
	helper.log_feature('test_elasticsearch_factory_2')
	time.sleep(1)
	helper.log_feature('test_elasticsearch_factory_3')
	time.sleep(1)
	helper.log_feature('test_elasticsearch_factory_4')
	helper.log_feature('test_elasticsearch_factory_5')
	pprint(helper.default_values)

def test_elasticsearch_factory_fail():
	passed = True
	try:
		helper = ElasticSearchHelper.get_instance(host=ELASTIC_SEARCH_HOST+'BOGUS', index='test_index')
		passed = False
	except Exception as e:
		helper = MockElasticSearchHelper()

	assert passed, "Should have failed and defaulted to Mock Class"
	helper.log_feature('test_elasticsearch_factory_0')
	helper.log_feature('test_elasticsearch_factory_1')
	time.sleep(1)
	helper.log_feature('test_elasticsearch_factory_2')
	time.sleep(1)
	helper.log_feature('test_elasticsearch_factory_3')
	time.sleep(1)
	helper.log_feature('test_elasticsearch_factory_4')
	helper.log_feature('test_elasticsearch_factory_5')
	pprint(helper.default_values)


def test_elasticsearch_two_step_construction():
	client = elasticsearch.Elasticsearch(hosts=[{'host': ELASTIC_SEARCH_HOST, 'port': 9200}], use_ssl=False,
	                                     verify_certs=True,
	                                     connection_class=elasticsearch.RequestsHttpConnection)
	helper = ElasticSearchHelper(client, index='test_index')
	helper.log_feature('test_elasticsearch_two_step_construction')


def test_elasticsearch_no_auto_flush():
	client = elasticsearch.Elasticsearch(hosts=[{'host': ELASTIC_SEARCH_HOST, 'port': 9200}], use_ssl=False,
	                                     verify_certs=True,
	                                     connection_class=elasticsearch.RequestsHttpConnection)
	helper = ElasticSearchHelper(client, index='test_index', auto_flush=False)
	helper.log_feature('test_elasticsearch_no_auto_flush')
	# we have to call flush_buffer to actually push data
	helper.flush_buffer()


def test_elasticsearch_flush():
	client = elasticsearch.Elasticsearch(hosts=[{'host': ELASTIC_SEARCH_HOST, 'port': 9200}], use_ssl=False,
	                                     verify_certs=True,
	                                     connection_class=elasticsearch.RequestsHttpConnection)
	helper = ElasticSearchHelper(client, index='test_index', auto_flush=False)
	helper.log_feature('test_elasticsearch_no_auto_flush')
	# we have to call flush_buffer to actually push data
	helper.flush_buffer()

def test_elasticsearch_decorator_pass():
	client = elasticsearch.Elasticsearch(hosts=[{'host': ELASTIC_SEARCH_HOST, 'port': 9200}], use_ssl=False,
	                                     verify_certs=True,
	                                     connection_class=elasticsearch.RequestsHttpConnection)
	helper = ElasticSearchHelper(client, index='test_index', auto_flush=True)

	@helper.log_feature_decorator("func_to_decorate", developer="gehad")
	def func_to_decorate():
		pass
	
	# calling function will add feature to buffer
	func_to_decorate()



def test_elasticsearch_own_decorator():
	client = elasticsearch.Elasticsearch(hosts=[{'host': ELASTIC_SEARCH_HOST, 'port': 9200}], use_ssl=False,
	                                     verify_certs=True,
	                                     connection_class=elasticsearch.RequestsHttpConnection)
	helper = ElasticSearchHelper(client, index='test_index', auto_flush=True)
	
	def elastic_global_feature_decorator(feature_name, **feature_kwargs):
		return helper.log_feature_decorator(feature_name, **feature_kwargs)
	
	@elastic_global_feature_decorator("elastic_global_feature_decorator", developer="gehad")
	def func_to_decorate_global():
		pass
	
	# calling function will add feature to buffer
	func_to_decorate_global()
