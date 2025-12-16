from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    calories_per_100g = models.IntegerField()
    unit = models.CharField(max_length=20)  

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.calories_per_100g} cal/100g)"