from django.db import models

class Answer(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=300, blank=True, null=True)
    is_answered = models.BooleanField(default=False)
