import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ApiKeys(APIView):
    def post(self, request, *args, **kwargs):
        key = request.data["key"]
        # response = save_key(key)
        # return Response(response, status=status.HTTP_200_OK, content_type="application/json")

    def get(self, request, *args, **kwargs):
        key_id = request.query_params.get("id")
        print(key_id)
        # response = get_key(key_id)
        # return Response(response, status=status.HTTP_200_OK, content_type="application/json")

