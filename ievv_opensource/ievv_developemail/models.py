from django.db import models


class DevelopEmail(models.Model):
    raw_content = models.TextField()

    created_datetime = models.DateTimeField(auto_now_add=True)
    from_email = models.TextField()
    recipients = models.TextField()
    message = models.TextField()
