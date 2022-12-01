from django.db import models
from django.urls import reverse

class Data(models.Model):
    consumed_quantity = models.CharField(max_length = 64)
    cost = models.CharField(max_length = 64)
    date = models.CharField(max_length = 64)
    instance_id = models.CharField(max_length = 64)
    meter_category = models.CharField(max_length = 64)
    resource_group = models.CharField(max_length = 64)
    resource_location = models.CharField(max_length = 64)
    tags_app_name = models.CharField(max_length = 64)
    tags_environment = models.CharField(max_length = 64)
    tags_business_unit = models.CharField(max_length = 64)
    unit_of_measure = models.CharField(max_length = 64)
    location = models.CharField(max_length = 64)
    service_name = models.CharField(max_length = 64)

    #need "slug" kwarg for app specific urls
    def get_absolute_url(self):
        return reverse("depth_view", kwargs={"slug": self.tags_app_name})
