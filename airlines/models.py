from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Airplane(models.Model):
    airplane_identifier = models.IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    passenger_capacity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.airplane_identifier} | ' \
               f'{self.passenger_capacity} | ' \
               f'{self.created}'
