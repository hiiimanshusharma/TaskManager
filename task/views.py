from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from .models import Task
from django.db.models import Q
from django.shortcuts import get_object_or_404


class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            user_id = request.user.id  # Assuming user ID is stored in the request object
            tasks = Task.objects.filter(user_id=user_id)



            serializer = TaskSerializer(tasks, many=True)  # Use many=True if there are multiple blogs

            return Response({
                'data': serializer.data,
                'message': 'tasks fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):
        try:
            data = request.data
            for key in ["task","description_text","is_completed"]:
                if key not in data:
                    return Response({'message' : f"Please provide '{key}' in request data"
                }, status = status.HTTP_400_BAD_REQUEST)
            data['user'] = request.user.id
            serializer  = TaskSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    # 'status': False,
                    'data' : serializer.errors,
                    'message' : 'something went wrong'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data' : serializer.data,
                'message' : 'blog created successfully'
            }, status = status.HTTP_201_CREATED)



        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)

    def patch(self, request, task_id):
        try:
            user_id = request.user.id
            task = get_object_or_404(Task, user_id=user_id, pk=task_id)
            serializer = TaskSerializer(task, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': 'Task updated successfully'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong while updating the task'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        try:
            user_id = request.user.id
            task = get_object_or_404(Task, user_id=user_id, pk=task_id)
            task.delete()
            return Response({
                'message': 'Task deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, uid):
    #     try:
    #         data = request.data
    #         for key in [ "is_completed"]:
    #             if key not in data:
    #                 return Response({'message' : f"Please provide '{key}' in request data"
    #             }, status = status.HTTP_400_BAD_REQUEST)
    #         task = Task.objects.filter(uid = data.get('uid'))
    #
    #         if not task.exists():
    #             return Response({
    #                 'data' : {},
    #                 'message' : 'invalid task uid'
    #             }, status = status.HTTP_400_BAD_REQUEST)
    #
    #         if request.user != task[0].user:
    #             return Response({
    #                 'data' : {},
    #                 'message' : 'you are not authorized to this'
    #             }, status = status.HTTP_400_BAD_REQUEST)
    #
    #         serializer  = TaskSerializer(task[0], data = data, partial = True)
    #
    #         if not serializer.is_valid():
    #             return Response({
    #                 'data' : serializer.errors,
    #                 'message' : 'something went wrong'
    #             }, status = status.HTTP_400_BAD_REQUEST)
    #
    #         serializer.save()
    #
    #         return Response({
    #             'data' : serializer.data,
    #             'message' : 'task updated successfully'
    #         }, status = status.HTTP_201_CREATED)
    #
    #     except Exception as e:
    #         print(e)
    #         return Response({
    #             'data' : {},
    #             'message' : 'something went wrong'
    #         }, status = status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, uid):
    #     try:
    #         data = request.data
    #
    #         task = Task.objects.filter(uid = data.get('uid'))
    #
    #         if not task.exists():
    #             return Response({
    #                 'data' : {},
    #                 'message' : 'invalid blog uid'
    #             }, status = status.HTTP_400_BAD_REQUEST)
    #
    #         if request.user != task[0].user:
    #             return Response({
    #                 'data' : {},
    #                 'message' : 'you are not authorized to this'
    #             }, status = status.HTTP_400_BAD_REQUEST)
    #
    #         task[0].delete()
    #         return Response({
    #             'data' : {},
    #             'message' : 'blog deleted successfully'
    #         }, status = status.HTTP_201_CREATED)
    #
    #     except Exception as e:
    #         print(e)
    #         return Response({
    #             'data' : {},
    #             'message' : 'something went wrong'
    #         }, status = status.HTTP_400_BAD_REQUEST)
