from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from notes.models import Image, User
from rest_framework_simplejwt.tokens import AccessToken
from notes.features.generate_random_string import generate_random_string


class ImageView(APIView):
    def post(self, request):
        token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
        user_id = token.payload["user_id"]
        image = request.data["image"]
        new_image = Image(id=generate_random_string(32), user_id=user_id, file=image)
        new_image.save()
        data = new_image.to_json()
        response = {"success": True, "data": {
            "id": data["id"],
        }}
        return Response(response, status=status.HTTP_200_OK, content_type="application/json")

    def get(self, request):
        image_id = request.query_params["id"]
        image = Image.objects.get(id=image_id)
        data = image.to_json()
        current_domain = request.get_host()
        image_url = data["file"].url
        response = {"success": True, "data": {
            "id": data["id"],
            "url": current_domain + image_url
        }}
        return Response(response, status=status.HTTP_200_OK, content_type="application/json")
