from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', blank= True, related_name="following")

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="poster")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Posted at")
    likes = models.ManyToManyField("User", related_name="likes", blank= True, null=True)

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.user.id,
            "poster": self.poster.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes.id,
        }