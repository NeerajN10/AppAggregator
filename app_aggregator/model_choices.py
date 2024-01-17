from django.db import models


class UserTypes(models.IntegerChoices):
    AGGREGATOR = 1, "AGGREGATOR"
    USER = 2, "USER"
