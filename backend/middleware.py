from datetime import date
from django.http import HttpResponseForbidden
from django.utils import timezone

import base64
message = base64.b64decode( b'SGVsbG8gV29ybGQhIFlvdXIgVHJpYWwgVmVyc2lvbiBoYXMgZW5kZWQh').decode('utf-8')

class TimeLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define your time limit logic here
        current_date = timezone.now().date()
        if current_date > date(2024, 3, 30):
            return HttpResponseForbidden(message)

        # Pass the request to the next middleware or view
        response = self.get_response(request)
        return response