from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError


class GptView(APIView):
    def post(self, request):
        try:
            data = self.get_data_from_request(request)
            response_data = {'message': data}
            return Response(response_data, status=status.HTTP_200_OK)
        except ParseError as e:
            return Response({'error': 'Ошибка в формате JSON'}, status=status.HTTP_400_BAD_REQUEST)

    def get_data_from_request(self, request):
        try:
            data = request.data
            return data
        except Exception as e:
            raise ParseError('Ошибка в формате JSON')
