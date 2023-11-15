from rest_framework.views import APIView
from notes.models import Note, Vault
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.response import Response
from notes.features.generate_id import generate_id


class NoteView(APIView):
    def post(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            title = request.data["title"]
            colors = ["#FFFFFF", "#0B6BCB", "#0B0D0E"]
            vault_id = request.query_params["vault_id"]

            vault = Vault.objects.get(id=vault_id, user_id=user_id)

            if not vault:
                response = {
                    "success": False,
                    "message": "Вы не имеете доступа к этому волту",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            new_note = Note(id=generate_id(), title=title, colors=colors, content=[], vault_id=vault_id)
            new_note.save()
            data = new_note.to_json()

            response = {
                "success": True,
                "message": "Ноут создан",
                "data": {
                    "id": data["id"],
                    "title": data["title"],
                    "colors": data["colors"]
                }
            }
            return Response(response, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось создать ноут",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    def get(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            note_id = request.query_params["id"]

            note = Note.objects.get(id=note_id)
            note_data = note.to_json()
            vault = note_data["vault"]
            vault_user = vault.user.to_json()
            is_public = vault.isPublic

            if not is_public and not vault_user["id"] == user_id:
                response = {
                    "success": False,
                    "message": "Не удалось получить ноут",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            response = {
                "success": True,
                "content": note_data["content"],
                "title": note_data["title"],
                "colors": note_data["colors"],
            }
            return Response(response, status=status.HTTP_200_OK, content_type="application/json")

        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось получить ноут",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    def delete(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            vault_id = request.query_params["vault_id"]
            note_id = request.query_params["note_id"]

            note = Note.objects.get(id=note_id, vault_id=vault_id)

            vault = note.to_json()["vault"]
            vault_data = vault.to_json()
            vault_user = vault_data["user"].to_json()

            if not note or not user_id == vault_user["id"]:
                response = {
                    "success": False,
                    "message": "Вы не имеете доступа к этому волту",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            note.delete()

            response = {
                "success": True,
                "message": "Ноут удален",
            }
            return Response(response, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось удалить ноут",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")


class GetByVault(APIView):
    def get(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            vault_id = request.query_params["id"]

            notes = Note.objects.filter(vault_id=vault_id).values('id', 'title')
            notes_data = []
            for note in notes:
                notes_data.append(note)

            vault = Vault.objects.get(id=vault_id)
            vault_user = vault.user.to_json()
            is_public = vault.isPublic

            if not is_public and not vault_user["id"] == user_id:
                response = {
                    "success": False,
                    "message": "Не удалось получить ноут",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            response = {
                "success": True,
                "content": notes_data
            }
            return Response(response, status=status.HTTP_200_OK, content_type="application/json")

        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось получить ноут",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")


class UpdateNote(APIView):
    def post(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            note_id = request.query_params["id"]
            title = request.data["title"]
            colors = request.data["colors"]
            content = request.data["content"]
            note = Note.objects.get(id=note_id)
            data = note.to_json()

            if not Note:
                response = {
                    "success": False,
                    "message": "Не удалось получить ноут",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            vault = data["vault"].to_json()
            vault_user = vault["user"].to_json()

            if not vault_user["id"] == user_id:
                response = {
                    "success": False,
                    "message": "Вы не имеете доступа к этому ноуту",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            note.title = title
            note.colors = colors
            note.content = content
            note.save()
            response = {
                "success": True,
                "message": "Ноут обновлен",
            }
            return Response(response, status=status.HTTP_200_OK, content_type="application/json")

        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось обновить ноут",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

