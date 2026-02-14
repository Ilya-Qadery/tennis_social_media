"""
Custom middleware for logging, security, and performance monitoring.
"""
import time
import uuid
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Log all API requests with timing and user context.
    Essential for debugging and performance monitoring.
    """

    def process_request(self, request: HttpRequest) -> None:
        request.start_time = time.time()
        request.request_id = str(uuid.uuid4())[:8]

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        if not hasattr(request, "start_time"):
            return response

        duration = time.time() - request.start_time
        user_id = getattr(request.user, "id", "anonymous")

        # Add headers for client-side debugging
        response["X-Request-ID"] = getattr(request, "request_id", "unknown")
        response["X-Response-Time"] = f"{duration:.3f}s"

        # Log slow requests (>500ms)
        if duration > 0.5:
            import logging
            logger = logging.getLogger("varzesha.performance")
            logger.warning(
                "Slow request",
                extra={
                    "request_id": getattr(request, "request_id", "unknown"),
                    "path": request.path,
                    "method": request.method,
                    "duration": duration,
                    "user_id": user_id,
                    "status_code": response.status_code,
                }
            )

        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses.
    """

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response