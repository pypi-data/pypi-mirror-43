# encoding: utf8

from django.conf import settings as django_settings

NUM_PROXIES = getattr(django_settings, 'NUM_PROXIES', None)

_DEFAULT_THROTTLE_RATES = {
    'user': None,
    'anon': None,
}
THROTTLE_RATES = getattr(django_settings, 'THROTTLE_RATES', _DEFAULT_THROTTLE_RATES)
THROTTLE_PROJECT = getattr(django_settings, 'THROTTLE_PROJECT', 'django')
_DEFAULT_THROTTLE_TRIGGER_RESPONSE = {
    'code': 'trigger_throttling',
    'description': '触发流控机制，请稍后重试...',
}
THROTTLE_TRIGGER_RESPONSE = getattr(django_settings, 'THROTTLE_TRIGGER_RESPONSE', _DEFAULT_THROTTLE_TRIGGER_RESPONSE)
