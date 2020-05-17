"""
Ghost: Boasts, Roasts
    Boolean if boast or roast
    Charfield for content of post
    integer field for up and down votes
    datetime field for submit time
"""
from django.db import models


class Post(models.Model):
    is_boast = models.BooleanField(default=True)
    content = models.CharField(max_length=280)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    total_votes = models.IntegerField(default=0)
    submit_time = models.DateTimeField(auto_now_add=True, blank=True)
    secret_key = models.CharField(max_length=6)

    @property
    def count(self):
        return self.up_votes - self.down_votes
