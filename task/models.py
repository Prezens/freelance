from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    consumer = models.ForeignKey(User, on_delete=models.CASCADE)
    executor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='executor')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.title

