from django.db import models

# Create your models here.


class ShareInfo(models.Model):
    name = models.CharField(max_length=50)
    info = models.JSONField()

    def __str__(self) -> str:
        return self.name