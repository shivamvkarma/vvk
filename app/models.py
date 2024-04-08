from django.db import models


class InstagramImage(models.Model):
    image = models.ImageField(upload_to='instagram_images/')
    instagram_post_url = models.URLField()

    def __str__(self):
        return f"Instagram Image {self.id}"
