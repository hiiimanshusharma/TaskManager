from django.urls import path
from task.views import TaskView

from task.views import TaskView


urlpatterns = [
    path('task/', TaskView.as_view(), name="task"),
    path('task/<uuid:task_id>/', TaskView.as_view(), name='task-detail'),
    # path('', PublicBlog.as_view()),
]
