from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import User
from ..validations.check_cyrillic import check_cyrillic
from ..features.generate_random_string import generate_random_string
from ..validations.check_json import check_json
import bcrypt


class Login(APIView):
    def post(self, request):
        nickname = request.data.nickname
        password = request.data.password
        user = User.objects.get(nickname=nickname)
        return Response(user, status=status.HTTP_200_OK, content_type="application/json")


class Registration(APIView):
    def post(self, request):
        nickname = request.data["nickname"]
        email = request.data["email"]
        password = request.data["password"]
        checkPassword = request.data["checkPassword"]

        if not password == checkPassword:
            response = {"success": False, "message": "Пароли не совпадают!"}
            return Response(response, status.HTTP_400_BAD_REQUEST, content_type="application/json")

        if len(password) < 8:
            response = {"success": False, "message": "Минимальная длина пароля 8 символов!"}
            return Response(response, status.HTTP_400_BAD_REQUEST, content_type="application/json")

        if check_cyrillic(password):
            response = {"success": False, "message": "В пароле не должно быть кириллических символов"}
            return Response(response, status.HTTP_400_BAD_REQUEST, content_type="application/json")

        if check_cyrillic(nickname):
            response = {"success": False, "message": "В никнейме не должно быть кириллических символов"}
            return Response(response, status.HTTP_400_BAD_REQUEST, content_type="application/json")

        filtered_nicknames = User.objects.filter(nickname=nickname)
        filtered_emails = User.objects.filter(email=email)

        if filtered_nicknames:
            response = {"success": False, "message": "Никнейм уже занят"}
            return Response(response, status.HTTP_400_BAD_REQUEST, content_type="application/json")

        if filtered_emails:
            response = {"success": False, "message": "Почта уже занята"}
            return Response(response, status.HTTP_400_BAD_REQUEST, content_type="application/json")

        password_bytes = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        new_user = User(id=generate_random_string(32), nickname=nickname, email=email, passwordHash=hashed_password)
        new_user.save()
        response = {"success": True, "message": "Вы зарегались!", "data": {
            "nickname": nickname,
            "email": email
        }}
        return Response(response, status.HTTP_200_OK, content_type="application/json")
