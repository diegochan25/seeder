from django.db import models


class SampleName(models.Model):
    class Types(models.IntegerChoices):
        NAME = (0, 'name')
        SURNAME = (1, 'surname')

    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField(choices=Types.choices, db_index=True)
    preferred_languages = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)