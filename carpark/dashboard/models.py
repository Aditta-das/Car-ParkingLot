from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class carPark(models.Model):
    car_no = models.CharField(null=True, max_length=20)
    slot_no = models.IntegerField(
        null=True,
        validators=[
            MaxValueValidator(8), 
            MinValueValidator(1)
            ]
        )
    ip_adress = models.GenericIPAddressField(null=True)
    def __str__(self):
        return f"car number {self.car_no}"    


class Information(models.Model):
    car_no = models.CharField(null=True, max_length=20)
    slot_no = models.IntegerField(
        null=True,
        validators=[
            MaxValueValidator(8), 
            MinValueValidator(1)
        ]
    )

class Rate(models.Model):
    visit = models.PositiveIntegerField(default=0)
    ip_adress = models.GenericIPAddressField(null=True)
    time_field = models.FloatField(null=True)

    def __str__(self):
        return f"{self.ip_adress}"