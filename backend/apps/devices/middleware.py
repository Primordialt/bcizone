class DeviceMetaMiddleware:
    """
    Attach basic device metadata to every request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR", "") or ""
        user_agent = request.META.get("HTTP_USER_AGENT", "") or ""
        request.device_meta = {"ip": ip, "user_agent": user_agent}
        return self.get_response(request)

