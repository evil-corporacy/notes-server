from rest_framework.views import APIView
from notes.models import Vault
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from rest_framework.response import Response


class VaultView(APIView):
    def post(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            print(token)
            user_id = token.payload["user_id"]
            title = request.data["title"]
            description = request.data["description"]
            isPublic = request.data["isPublic"]
            tags = request.data["tags"]
            colors = request.data["colors"]

            new_vault = Vault(user_id=user_id, title=title, description=description, isPublic=isPublic, tags=tags, colors=colors)
            new_vault.save()
            data = new_vault.to_json()

            response = {
                "success": True,
                "message": "Волт " + title + " создан",
                "data": {
                    "id": data["id"],
                    "title": data["title"],
                    "description": data["description"],
                    "tags": data["tags"],
                    "isPublic": data["isPublic"],
                    "colors": data["colors"]
                }
            }

            return Response(response, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось создать волт",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    def get(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            vault_id = request.query_params["id"]

            data = Vault.objects.get(id=vault_id)

            is_public = data.isPublic

            if not is_public:
                if user_id == data.user_id:
                    json_data = data.to_json()
                    response = {
                        "success": True,
                        "data": {
                            "title": json_data["title"],
                            "description": json_data["description"],
                            "id": json_data["id"],
                            "colors": json_data["colors"],
                            "tags": json_data["tags"],
                        }
                    }
                    return Response(response, status=status.HTTP_200_OK, content_type="application/json")
                else:
                    response = {
                        "success": False,
                        "message": "Вы не имеете доступа к этому волту"
                    }
                    return Response(response, status=status.HTTP_200_OK, content_type="application/json")

            json_data = data.to_json()
            response = {
                "success": True,
                "data": {
                    "title": json_data["title"],
                    "description": json_data["description"],
                    "id": json_data["id"],
                    "colors": json_data["colors"],
                    "tags": json_data["tags"],
                }
            }

            return Response(response, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось получить волт",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

    def delete(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]
            vault_id = request.query_params["vault_id"]

            vault = Vault.objects.get(id=vault_id, user_id=user_id)

            if not vault:
                response = {
                    "success": False,
                    "message": "Вы не имеете доступа к этому волту",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

            vault.delete()

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


class GetUserVaults(APIView):
    def get(self, request):
        try:
            token = AccessToken(request.headers["Authorization"].replace("Bearer ", ""))
            user_id = token.payload["user_id"]

            data = Vault.objects.filter(user_id=user_id)

            formatted_data = []

            for element in data:
                element = element.to_json()

                formatted_element = {
                    "id": element["id"],
                    "title": element["title"],
                    "description": element["description"],
                    "isPublic": element["isPublic"],
                    "colors": element["colors"],
                    "tags": element["tags"]
                }
                formatted_data.append(formatted_element)

            print(formatted_data)

            response = {
                "success": True,
                "data": formatted_data
            }

            return Response(response, status=status.HTTP_200_OK, content_type="application/json")
        except Exception as e:
            response = {
                "success": False,
                "message": "Не удалось получить волты",
                "error": str(e)
            }
            print(e)
            return Response(response, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")

