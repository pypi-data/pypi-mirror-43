# encoding: utf8

from django.http.response import JsonResponse

from .throttling import AnonRateThrottle
from .settings import THROTTLE_TRIGGER_RESPONSE


class AnonThrottleMiddleware(object):
    def process_request(self, request):
        if not AnonRateThrottle().allow_request(request, None):
            return JsonResponse(THROTTLE_TRIGGER_RESPONSE)
