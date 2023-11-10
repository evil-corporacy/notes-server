from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from openai import OpenAI
from notes.models import User
from rest_framework.response import Response
from rest_framework import status


class ApiKeys(APIView):
    def post(self, request, *args, **kwargs):
        token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
        user_id = token.payload["user_id"]
        key = request.data["key"]
        client = OpenAI()

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": ""
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
        except Exception as e:


        user = User.objects.get(id=user_id).to_json()

        response = {"success": True, "message": "Ключ OpenAI сохранен", "key": key}
        return Response(response, status=status.HTTP_200_OK, content_type="application/json")

    def get(self, request, *args, **kwargs):
        key_id = request.query_params.get("id")
        print(key_id)
        # response = get_key(key_id)
        # return Response(response, status=status.HTTP_200_OK, content_type="application/json")

