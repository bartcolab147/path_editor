from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class BackgroundImage(models.Model):
    image = models.ImageField(upload_to='backgrounds/')
    name = models.CharField(max_length=100)
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        self.width, self.height = img.size
        super().save(update_fields=['width', 'height'])

    def __str__(self):
        return self.name
    
    """ Returns the number of routes associated with this background image """
    def route_count(self):
        return self.route_set.count()

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    background = models.ForeignKey(BackgroundImage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Point(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='points')
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"({self.x}, {self.y})"
