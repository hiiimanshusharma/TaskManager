from django.db import models
import uuid
from django.contrib.auth.models import User

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Task(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=500)
    description_text = models.TextField()
    is_completed = models.BooleanField(default=False)
