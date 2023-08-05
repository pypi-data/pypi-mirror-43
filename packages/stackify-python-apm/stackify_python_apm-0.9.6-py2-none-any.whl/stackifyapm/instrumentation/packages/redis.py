from __future__ import absolute_import

from stackifyapm.instrumentation.packages.base import AbstractInstrumentedModule
from stackifyapm.traces import CaptureSpan
from stackifyapm.utils import compat, get_method_name


class Redis3CheckMixin(object):
    instrument_list_3 = []
    instrument_list = []

    def get_instrument_list(self):
        try:
            from redis import VERSION

            if VERSION[0] >= 3:
                return self.instrument_list_3
            return self.instrument_list
        except ImportError:
            return self.instrument_list


class RedisInstrumentation(Redis3CheckMixin, AbstractInstrumentedModule):
    name = "redis"

    instrument_list_3 = [("redis.client", "Redis.execute_command")]
    instrument_list = [("redis.client", "Redis.execute_command"), ("redis.client", "StrictRedis.execute_command")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        if len(args) > 0:
            wrapped_name = str(args[0])
        else:
            wrapped_name = self.get_wrapped_name(wrapped, instance, method)

        extra_data = {
            "wrapped_method": "execute",
            "provider": self.name,
            "type": "Cache",
            "sub_type": "cache",
            "operation": args and args[0] and args[0].lower() or get_method_name(method),
        }

        cache_name = len(args) > 1 and args[1] or None
        if cache_name:
            if isinstance(cache_name, compat.string_types):
                extra_data['cache_name'] = cache_name
                extra_data['cache_key'] = cache_name.split(':')[-1]
            elif isinstance(cache_name, compat.list_type):
                extra_data['cache_name'] = cache_name
                extra_data['cache_key'] = [name.split(':')[-1] for name in cache_name]
            elif isinstance(cache_name, compat.dict_type):
                extra_data['cache_name'] = list(cache_name.keys())
                extra_data['cache_key'] = [name.split(':')[-1] for name in cache_name.keys()]
            else:
                extra_data['cache_key'] = cache_name

        with CaptureSpan(wrapped_name, "cache.redis", extra_data, leaf=True):
            return wrapped(*args, **kwargs)


class RedisPipelineInstrumentation(Redis3CheckMixin, AbstractInstrumentedModule):
    name = "redis"

    instrument_list_3 = [("redis.client", "Pipeline.execute")]
    instrument_list = [("redis.client", "BasePipeline.execute")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        wrapped_name = self.get_wrapped_name(wrapped, instance, method)
        extra_data = {
            "wrapped_method": "execute",
            "provider": self.name,
            "type": "Cache",
            "sub_type": "cache",
            "operation": args and args[0] and args[0].lower() or get_method_name(method),
        }

        cache_name = len(args) > 1 and args[1] or None
        if cache_name:
            if isinstance(cache_name, compat.string_types):
                extra_data['cache_name'] = cache_name
                extra_data['cache_key'] = cache_name.split(':')[-1]
            elif isinstance(cache_name, compat.list_type):
                extra_data['cache_name'] = cache_name
                extra_data['cache_key'] = [name.split(':')[-1] for name in cache_name]
            elif isinstance(cache_name, compat.dict_type):
                extra_data['cache_name'] = list(cache_name.keys())
                extra_data['cache_key'] = [name.split(':')[-1] for name in cache_name.keys()]
            else:
                extra_data['cache_key'] = cache_name

        with CaptureSpan(wrapped_name, "cache.redis", extra_data, leaf=True):
            return wrapped(*args, **kwargs)
