# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils.functional import lazy
from six import text_type as str

JS_VAR_NAME = lazy(
    lambda: str(getattr(settings, 'JS_REVERSE_JS_VAR_NAME', 'Urls')),
    str)()
JS_AVAILABLE_NAMESPACES = lazy(
    lambda: getattr(settings, 'JS_REVERSE_AVAILABLE_NAMESPACES', []),
    list, tuple)()
