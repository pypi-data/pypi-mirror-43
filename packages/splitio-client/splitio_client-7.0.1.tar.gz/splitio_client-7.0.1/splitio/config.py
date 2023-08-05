"""Default settings for the Split.IO SDK Python client"""
from __future__ import absolute_import, division, print_function, unicode_literals

import importlib
import logging
import json

from .version import __version__
from splitio.utils import get_hostname, get_ip

logger = logging.getLogger(__name__)

SDK_API_BASE_URL = 'https://sdk.split.io/api'
EVENTS_API_BASE_URL = 'https://events.split.io/api'

SDK_VERSION = 'python-{package_version}'.format(package_version=__version__)

DEFAULT_CONFIG = {
    'connectionTimeout': 1500,
    'sdkApiBaseUrl': SDK_API_BASE_URL,
    'eventsApiBaseUrl': EVENTS_API_BASE_URL,
    'splitSdkMachineName': None,
    'splitSdkMachineIp': None,
    'readTimeout': 1500,
    'featuresRefreshRate': 5,
    'segmentsRefreshRate': 60,
    'metricsRefreshRate': 60,
    'impressionsRefreshRate': 60,
    'randomizeIntervals': False,
    'maxImpressionsLogSize': -1,
    'maxMetricsCallsBeforeFlush': 1000,
    'ready': 0,
    'redisHost': 'localhost',
    'redisPort': 6379,
    'redisDb': 0,
    'redisPassword': None,
    'redisSocketTimeout': None,
    'redisSocketConnectTimeout': None,
    'redisSocketKeepalive': None,
    'redisSocketKeepaliveOptions': None,
    'redisConnectionPool': None,
    'redisUnixSocketPath': None,
    'redisEncoding': 'utf-8',
    'redisEncodingErrors': 'strict',
    'redisCharset': None,
    'redisErrors': None,
    'redisDecodeResponses': False,
    'redisRetryOnTimeout': False,
    'redisSsl': False,
    'redisSslKeyfile': None,
    'redisSslCertfile': None,
    'redisSslCertReqs': None,
    'redisSslCaCerts': None,
    'redisMaxConnections': None,
    'eventsPushRate': 60,
    'eventsQueueSize': 500,
}

MAX_INTERVAL = 180


GLOBAL_KEY_PARAMETERS = {
    'sdk-language-version': SDK_VERSION,
    'instance-id': get_hostname(),
    'ip-address': get_ip(),
}


def set_machine_ip(machine_ip):
    if machine_ip:
        GLOBAL_KEY_PARAMETERS['ip-address'] = machine_ip


def set_machine_name(machine_name):
    if machine_name:
        GLOBAL_KEY_PARAMETERS['instance-id'] = machine_name


def parse_config_file(filename):
    """Reads a Splitio JSON config file, like the following:

    {
      "apiKey": "some-api-key",
      "sdkApiBaseUrl": "https://sdk-loadtesting.split.io/api",
      "eventsApiBaseUrl": "https://events-loadtesting.split.io/api",
      "connectionTimeout": 1500,
      "readTimeout": 1500,
      "featuresRefreshRate": 5,
      "segmentsRefreshRate": 60,
      "metricsRefreshRate": 60,
      "impressionsRefreshRate": 60,
      "randomizeIntervals": False,
      "maxImpressionsLogSize": -1,
      "maxMetricsCallsBeforeFlush": 1000,
      "ready": 0,
      "redisFactory": "some.python.function",
      "redisHost": "locahost",
      "redisPort": 6379,
      "redisDb": 0
    }

    :param filename: Name of the config file
    :type filename: str
    :return: A config dictionary
    :rtype: dict
    """
    config = DEFAULT_CONFIG.copy()

    try:
        with open(filename) as fp:
            json_config = json.load(fp)
            config.update(json_config)
            if 'splitSdkMachineName' in config:
                set_machine_name(config['splitSdkMachineName'])
            if 'splitSdkMachineIp' in config:
                set_machine_ip(config['splitSdkMachineIp'])
    except Exception:
        logger.error('There was a problem reading the config file: %s', filename)
        return DEFAULT_CONFIG.copy()

    return config


def import_from_string(val, setting_name):
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(
            "Could not import '%s' for SPLITIO setting '%s'. %s: %s." % (val, setting_name,
                                                                         e.__class__.__name__, e))
