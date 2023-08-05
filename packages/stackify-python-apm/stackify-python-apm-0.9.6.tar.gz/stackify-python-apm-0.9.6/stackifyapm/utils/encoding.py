# -*- coding: utf-8 -*-
import datetime
import uuid
from decimal import Decimal

from stackifyapm.conf.constants import KEYWORD_MAX_LENGTH
from stackifyapm.utils import compat

PROTECTED_TYPES = compat.integer_types + (type(None), float, Decimal, datetime.datetime, datetime.date, datetime.time)


def is_protected_type(obj):
    return isinstance(obj, PROTECTED_TYPES)


def force_text(s, encoding="utf-8", strings_only=False, errors="strict"):
    if isinstance(s, compat.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, compat.string_types):
            if hasattr(s, "__unicode__"):
                s = s.__unicode__()
            else:
                if compat.PY3:
                    if isinstance(s, bytes):
                        s = compat.text_type(s, encoding, errors)
                    else:
                        s = compat.text_type(s)
                else:
                    s = compat.text_type(bytes(s), encoding, errors)
        else:
            s = s.decode(encoding, errors)
    except UnicodeDecodeError as e:
        if not isinstance(s, Exception):
            raise UnicodeDecodeError(*e.args)
        else:
            s = " ".join([force_text(arg, encoding, strings_only, errors) for arg in s])
    return s


def _has_stackifyapm_metadata(value):
    try:
        return callable(value.__getattribute__("__stackifyapm__"))
    except Exception:
        return False


def transform(value, context=None):
    if context is None:
        context = {}

    objid = id(value)
    if objid in context:
        return "<...>"

    context[objid] = 1
    transform_rec = lambda o: transform(o, context)  # noqa

    if isinstance(value, (tuple, list, set, frozenset)):
        try:
            ret = type(value)(transform_rec(o) for o in value)
        except Exception:
            class value_type(list):
                __name__ = type(value).__name__

            ret = value_type(transform_rec(o) for o in value)
    elif isinstance(value, uuid.UUID):
        ret = repr(value)
    elif isinstance(value, dict):
        ret = dict((to_unicode(k), transform_rec(v)) for k, v in compat.iteritems(value))
    elif isinstance(value, compat.text_type):
        ret = to_unicode(value)
    elif isinstance(value, compat.binary_type):
        ret = to_string(value)
    elif not isinstance(value, compat.class_types) and _has_stackifyapm_metadata(value):
        ret = transform_rec(value.__stackifyapm__())
    elif isinstance(value, bool):
        ret = bool(value)
    elif isinstance(value, float):
        ret = float(value)
    elif isinstance(value, int):
        ret = int(value)
    elif compat.PY2 and isinstance(value, long):  # noqa F821
        ret = long(value)  # noqa F821
    elif value is not None:
        try:
            ret = transform(repr(value))
        except Exception:
            ret = u"<BadRepr: {}>".format(type(value))
    else:
        ret = None
    del context[objid]
    return ret


def to_unicode(value):
    try:
        value = compat.text_type(force_text(value))
    except (UnicodeEncodeError, UnicodeDecodeError):
        value = "(Error decoding value)"
    # swallow unexpected exception
    except Exception:
        try:
            value = compat.binary_type(repr(type(value)))
        except Exception:
            value = "(Error decoding value)"
    return value


def to_string(value):
    try:
        return compat.binary_type(value.decode("utf-8").encode("utf-8"))
    except Exception:
        return to_unicode(value).encode("utf-8")


def keyword_field(string):
    if not isinstance(string, compat.string_types) or len(string) <= KEYWORD_MAX_LENGTH:
        return string
    return string[: KEYWORD_MAX_LENGTH - 1] + u"…"
