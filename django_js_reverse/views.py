#-*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from itertools import chain, count
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from six.moves import zip
import six
from .settings import JS_VAR_NAME, JS_AVAILABLE_NAMESPACES

def urls_js(request):
    if not re.match(r'^[$A-Z_][\dA-Z_$]*$', JS_VAR_NAME.upper()):
        raise ImproperlyConfigured(
            'JS_REVERSE_JS_VAR_NAME setting "%s" is not a valid javascript identifier.' % (JS_VAR_NAME))

    # Returns list of tuples [(<url_name>, <namespace_path>, <url_patern_tuple> ), ...]
    prepare_url_list = lambda urlresolver, namespace_path='', namespace='': [
        (namespace + url_name, namespace_path, url_pattern[0][0])
        for url_name, url_pattern in urlresolver.reverse_dict.items()
        if (isinstance(url_name, str) or isinstance(url_name, unicode))
    ]


    def serialize_urlresolver(namespace, pathprefix, urlresolver):
        nsprefix = '' if namespace is None else namespace + ':'
        if namespace in JS_AVAILABLE_NAMESPACES or not namespace:
            for url_name, url_pattern in urlresolver.reverse_dict.items():
                if isinstance(url_name, basestring):
                    yield (nsprefix + url_name, pathprefix, url_pattern[0][0])

        for child_ns, (child_ns_path, child_urlresolver) in \
            urlresolver.namespace_dict.items():

            for args in serialize_urlresolver(nsprefix + child_ns,
                                              pathprefix + child_ns_path,
                                              child_urlresolver):
                yield args

    default_urlresolver = urlresolvers.get_resolver(None)
    url_lists = serialize_urlresolver(None, '', default_urlresolver)

    return render_to_response('django_js_reverse/urls_js.tpl',
                              {
                                  'urls': url_lists,
                                  'url_prefix': urlresolvers.get_script_prefix(),
                                  'js_var_name': JS_VAR_NAME
                              },
                              context_instance=RequestContext(request), content_type='application/javascript')
