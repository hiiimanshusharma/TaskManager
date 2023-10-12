from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status


def validate_request(fields):
        for key in fields:
            if key not in self.request_data:
                return Response({'message' : f"Please provide '{key}' in request data"
            }, status = status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):


    def post(self, request):
        try:
            data = request.data
            for key in ["first_name" ,"last_name" ,    "username", "password"]:
                if key not in data:
                    return Response({'message' : f"Please provide '{key}' in request data"
                }, status = status.HTTP_400_BAD_REQUEST)
            # validate_request(fields= ["first_name" ,"last_name" ,    "username", "password"])


            serializer = RegisterSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data' : {},
                'message' : 'your account is created'
            }, status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        try:
            data = request.data
            for key in ["username", "password"]:
                if key not in data:
                    return Response({'message' : f"Please provide '{key}' in request data"
                }, status = status.HTTP_400_BAD_REQUEST)
            # validate_request(fields= ["username", "password"])

            serializer = LoginSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'invalid credentials'
                }, status = status.HTTP_400_BAD_REQUEST)

            response = serializer.get_jwt_token(serializer.data)

            return Response(response, status = status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
