from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from uuid import uuid4  # Import uuid4 to generate real UUIDs
from .views import TaskView
from .serializers import TaskSerializer
from django.urls import reverse
from django.shortcuts import get_object_or_404

class TaskViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.task1 = Task.objects.create(
            user=self.user,
            task="Sample Task 1",
            description_text="Description for Sample Task 1",
            is_completed=False
        )
        self.task1.save()
        self.task2 = Task.objects.create(
            user=self.user,
            task="Sample Task 2",
            description_text="Description for Sample Task 2",
            is_completed=True
        )
        self.task2.save()
        self.task3 = Task.objects.create(
            user=self.user,
            task="Sample Task 3",
            description_text="Description for Sample Task 3",
            is_completed=True
        )
        self.task3.save()

        self.client.force_authenticate(user=self.user)


    def test_get_task_list(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Send a GET request to the task list endpoint
        response = self.client.get(reverse("task"))

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response contains the expected data
        self.assertEqual(len(response.data['data']), 3)

    def test_create_task(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Data for creating a new task with a custom 'uid' value
        # task_uuid = uuid4()
        data = {
            "task": "Task 4",
            "description_text": "Description for Task 3",
            "is_completed": False
        }

        # Send a POST request to create a new task
        response = self.client.post(reverse("task"), data, format='json')

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the task was created in the database
        task = Task.objects.get(task="Task 4")
        self.assertEqual(str(task.uid), response.data["data"]["uid"])

    def test_patch_task(self):
        updated_data = {
            "task": "Updated Task",
            "is_completed": True
        }
        url = reverse('task-detail', args=[str(self.task2.uid)])
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Task updated successfully')
        self.task2.refresh_from_db()
        self.assertEqual(self.task2.task, "Updated Task")
        self.assertEqual(self.task2.is_completed, True)

    def test_delete_task(self):
        url = reverse('task-detail', args=[str(self.task3.uid)])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(uid=self.task3.uid).exists())

class TaskSerializerTest(TestCase):
    def test_valid_serializer(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        data = {
            "task": "Sample Task",
            "description_text": "This is a sample task description.",
            "is_completed": False,
            "user": user.id
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid(), f"Serializer is not valid. Errors: {serializer.errors}")

    def test_invalid_serializer(self):
        data = {
            "task": "",
            "description_text": "This is a sample task description.",
            "is_completed": False,
            "user": 1
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid(), f"Serializer is unexpectedly valid.")
