from django.db import models


class Schema(models.Model):
    id = models.BigAutoField(primary_key=True)

    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    # Annotations
    owner_id: int

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schemas'
        constraints = [models.UniqueConstraint(fields=['owner_id', 'name'], name='uniq_schema_name_per_owner')]