from django.conf import settings
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(request):
    """Infrastructure liveness probe. No DB, auth, or secrets."""
    return JsonResponse({"status": "ok"})


def sentry_test_error(request):
    """
    Intentionally raises so Sentry can be verified.

    Allowed when DEBUG is True (local) or ENABLE_SENTRY_TEST_ENDPOINT is set.
    Disabled in production by default.
    """
    if not (settings.DEBUG or getattr(settings, "ENABLE_SENTRY_TEST_ENDPOINT", False)):
        raise Http404()
    raise Exception("Sentry test error")
