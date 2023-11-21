from django.http import HttpResponse

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Добавляем заголовки CORS для всех ответов
        response['Access-Control-Allow-Origin'] = 'https://ec-notes-client.vercel.app'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        response['Access-Control-Allow-Credentials'] = 'true'

        return response
