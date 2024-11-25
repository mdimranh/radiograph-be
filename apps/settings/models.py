from django.db import models

class siteConfig(models.Model):
    logo = models.ImageField(upload_to="site_config/", null=True, blank=True)
    favicon = models.ImageField(upload_to="site_config/", null=True, blank=True)
    default_color = models.CharField(max_length=20, default="#FFFFFF")
    title = models.CharField(max_length=255, default="My Site")

    def save(self, *args, **kwargs):
        if not self.pk and siteConfig.objects.exists():
            raise ValueError("There can only be one Site Configuration instance.")
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        # Create the singleton instance if it doesn't exist
        instance, created = cls.objects.get_or_create(pk=1)
        return instance

    def __str__(self):
        return "Site Configuration"
