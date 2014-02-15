#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url


ns2 = patterns(
    '',
    url(r'^bar/$', 'bar', name='bar'),
)

ns1 = patterns(
    '',
    url(r'^foo/$', 'foo', name='foo'),
    url(r'^ns2/', include(ns2, namespace='ns2'))
)

urlpatterns = patterns(
    '',
    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

    # test urls
    url(r'^test_no_url_args/$', 'foo', name='test_no_url_args'),
    url(r'^test_one_url_args/(?P<arg_one>[-\w]+)/$', 'foo',
        name='test_one_url_args'),
    url(r'^test_two_url_args/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', 'foo',
        name='test_two_url_args'),

    url(r'^ns1/',
        include(ns1, namespace='ns1')),
)
