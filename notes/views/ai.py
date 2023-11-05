import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
import openai
import json
from notes.shared.data.openai_instruction import instruction
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_text(messages):
    formatted_messages = [{"role": "system", "content": instruction}]
    for message in messages:
        formatted_messages.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=formatted_messages
    )

    if response.choices and response.choices[0].message and response.choices[0].message.content:
        answer = response.choices[0].message.content
        try:
            print(answer)
            return json.loads(answer)
        except json.JSONDecodeError as e:
            return {"error": True}
    else:
        return {"error": True}


class GenerateText(APIView):
    def post(self, request):
        try:
            data = request.data
            messages = data.get("messages", [])
            prompt = data.get("prompt", '')
            messages.append(prompt)
            answer = generate_text(messages)
            response = {"success": True, "answer": answer}
            return Response(response, status=status.HTTP_200_OK, content_type="application/json")
        except ParseError as e:
            return Response({'error': 'Ошибка в формате JSON'}, status=status.HTTP_400_BAD_REQUEST,
                            content_type="application/json")

    def get_data_from_request(self, request):
        try:
            data = request.data
            return data
        except Exception as e:
            raise ParseError('Ошибка в формате JSON')
