from django.db import models


class InstagramImage(models.Model):
    image = models.ImageField(upload_to='instagram_images/')
    instagram_post_url = models.URLField()

    def __str__(self):
        return f"Instagram Image {self.id}"

class SubBanners(models.Model):
    image = models.ImageField(upload_to='sub-banners/')
    discount = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
