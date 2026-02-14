"""
Custom rate throttling for Iranian market requirements.
"""
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.request import Request


class SMSRateThrottle(SimpleRateThrottle):
    """
    Strict rate limiting for SMS endpoints to prevent pumping attacks.
    Scope: 'sms' - 5 per hour per phone number.
    """
    scope = "sms"
    cache_format = "throttle_%(scope)s_%(ident)s"

    def get_cache_key(self, request: Request, view) -> str:
        # Rate limit by phone number in request data
        phone = request.data.get("phone", self.get_ident(request))
        return self.cache_format % {
            "scope": self.scope,
            "ident": phone,
        }


class AnonBurstRateThrottle(SimpleRateThrottle):
    """
    Burst protection for anonymous users - stricter limits.
    """
    scope = "anon_burst"
    rate = "10/minute"

    def get_cache_key(self, request: Request, view) -> str:
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }