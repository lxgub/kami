from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Airplane(models.Model):
    plain_identifier = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    passenger_capacity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.plain_identifier} | ' \
               f'{self.passenger_capacity} | ' \
               f'{self.created}'
