from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    level = models.CharField(max_length=50) #Beginner, Intermediate, Advanced
    prerequisites = models.TextField(blank=True)

    def __str__(self):
        return self.name