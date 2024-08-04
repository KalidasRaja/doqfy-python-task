from django.db import models

class Snippet(models.Model):
    content = models.TextField()
    key = models.CharField(max_length=32, blank=True, null=True)
    snippet_id = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.snippet_id
