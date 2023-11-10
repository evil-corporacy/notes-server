from django.http import JsonResponse


class ErrorValidation:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            response = JsonResponse({"success": False, "error": str(e)}, status=500)
        return response
