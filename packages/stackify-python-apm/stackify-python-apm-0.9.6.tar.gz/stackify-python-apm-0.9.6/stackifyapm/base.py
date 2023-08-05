from __future__ import absolute_import

import logging
import os
import platform
import socket
import sys

import stackifyapm
from stackifyapm.conf import Config
from stackifyapm.conf.constants import TRACE_CONTEXT_VERSION
from stackifyapm.traces import Tracer
from stackifyapm.utils.encoding import keyword_field

__all__ = ("Client",)


class Client(object):
    """
    The base StackifyAPM client, which handles loggings.

    Provides process, system and applicaiton info.
    """

    logger = logging.getLogger("stackifyapm")

    def __init__(self, config=None, **kwargs):
        self._service_info = None

        self.error_logger = logging.getLogger("stackifyapm.errors")
        self.apm_logger = logging.getLogger('stackify_apm')
        self.config = Config(config, inline_dict=kwargs)
        if self.config.errors:
            for msg in self.config.errors.values():
                self.error_logger.error(msg)

        self.tracer = Tracer(
            logger=self.log,
            sample_rate=self.config.transaction_sample_rate,
        )

    def log(self, data):
        self.apm_logger.debug(data)

    def begin_transaction(self, transaction_type, trace_parent=None, client=None):
        return self.tracer.begin_transaction(transaction_type, trace_parent=trace_parent, client=client)

    def end_transaction(self, name=None, result=None):
        return self.tracer.end_transaction(result, name)

    def capture_exception(self, exception=None, **kwargs):
        return self.tracer.capture_exception(exception=exception)

    def get_service_info(self):
        if self._service_info:
            return self._service_info

        language_version = platform.python_version()
        if hasattr(sys, "pypy_version_info"):
            runtime_version = ".".join(map(str, sys.pypy_version_info[:3]))
        else:
            runtime_version = language_version

        result = {
            "name": keyword_field(self.config.service_name),
            "environment": keyword_field(self.config.environment),
            "version": keyword_field(self.config.service_version),
            "agent": {
                "name": "python",
                "version": stackifyapm.VERSION or TRACE_CONTEXT_VERSION or 'unknown',
            },
            "language": {
                "name": "python",
                "version": keyword_field(platform.python_version()),
            },
            "runtime": {
                "name": keyword_field(platform.python_implementation()),
                "version": keyword_field(runtime_version),
            },
        }

        if self.config.framework_name:
            result["framework"] = {
                "name": keyword_field(self.config.framework_name),
                "version": keyword_field(self.config.framework_version),
            }

        self._service_info = result
        return result

    def get_process_info(self):
        return {
            "pid": os.getpid(),
            "ppid": os.getppid() if hasattr(os, "getppid") else None,
            "argv": sys.argv,
        }

    def get_system_info(self):
        return {
            "hostname": keyword_field(socket.gethostname()),
            "architecture": platform.machine(),
            "platform": platform.system().lower(),
        }

    def get_application_info(self):
        return {
            "application_name": self.config.application_name,
            "base_dir": self.config.base_dir,
            "environment": not self.config.environment == 'None' and self.config.environment or 'Test',
        }
