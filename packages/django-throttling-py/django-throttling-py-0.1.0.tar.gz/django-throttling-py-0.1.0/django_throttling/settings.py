# encoding: utf8

from django.conf import settings as django_settings

NUM_PROXIES = django_settings.get('NUM_PROXIES', None)

_DEFAULT_THROTTLE_RATES = {
    'user': None,
    'anon': None,
}
THROTTLE_RATES = django_settings.get('THROTTLE_RATES', _DEFAULT_THROTTLE_RATES)
THROTTLE_PROJECT = django_settings.get('THROTTLE_PROJECT', 'django')
_DEFAULT_THROTTLE_TRIGGER_RESPONSE = {
    'code': 'trigger_throttling',
    'description': '触发流控机制，请稍后重试...',
}
THROTTLE_TRIGGER_RESPONSE = django_settings.get('THROTTLE_TRIGGER_RESPONSE', _DEFAULT_THROTTLE_TRIGGER_RESPONSE)
