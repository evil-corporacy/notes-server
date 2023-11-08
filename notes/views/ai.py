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


def get_key(id):
    return {"success": True, "message": "Ключ получен", "key": "213123213", "keyId": id}


def save_key(key):
    return {"success": True, "message": "Ключ сохранен", "key": key}


def get_chat(id):
    return {"id": id}


def flatten_content(content):
    if isinstance(content, list):
        return " ".join(flatten_content(item["content"]) for item in content)
    elif isinstance(content, dict):
        return flatten_content(content["content"])
    elif isinstance(content, str):
        return content
    else:
        return str(content)


def generate_text(messages):
    try:
        for message in messages:
            message["content"] = flatten_content(message["content"])

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": instruction}] + messages
        )
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content
            try:
                return json.loads(answer)
            except json.JSONDecodeError as e:
                return [{'type': 'heading-1', 'content': 'Ошибка генерации текста'}, {'type': 'text', 'content': 'Возникла ошибка при генерации текста. Пожалуйста, попробуйте еще раз.'}]
        else:
            return [{'type': 'heading-1', 'content': 'Ошибка генерации текста'}, {'type': 'text', 'content': 'Возникла ошибка при генерации текста. Пожалуйста, попробуйте еще раз.'}]
    except ParseError as e:
        return {"error": True, "message": e}


class Ai(APIView):
    def post(self, request, *args, **kwargs):
        try:
            chat_id = request.query_params.get("id")
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

    def get(self, request, *args, **kwargs):
        try:
            chat_id = request.query_params.get("id")
            response = get_chat(chat_id)
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
