# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from notes.models import User
#
#
# class CheckAuth:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         token_key = request.META.get("HTTP_AUTHORIZATION")
#
#         if token_key:
#             if token_key.startswith("Bearer "):
#                 token_key = token_key[7:]
#
#             try:
#                 token = User.objects.get(id=)
#
#                 if not token.user.is_active:
#                     response = {"success": False, "message": "Вы не авторизованы"}
#                     return Response(response, status=status.HTTP_401_UNAUTHORIZED)
#             except ConnectionError as e:
#                 response = {"success": False, "message": "Вы не авторизованы"}
#                 return Response(response, status=status.HTTP_401_UNAUTHORIZED)
#
#         return self.get_response(request)
