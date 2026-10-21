from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import RelatedManager, ManyRelatedManager

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Annotations
    userrole_set: 'ManyRelatedManager[UserRole]'
    accounttoken_set: 'RelatedManager[AccountToken]'

    USERNAME_FIELD = 'email'

    def initials(self) -> str:
        initials = ''
        if self.first_name:
            initials += self.first_name[0].upper()
        if self.last_name:
            initials += self.last_name[0].upper()
        return initials

class UserRole(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'role_id')

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    permissions = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccountToken(models.Model):
    class Types(models.IntegerChoices):
        EMAIL_VERIFICATION = (0, 'email verification')
        PASSWORD_RESET = (1, 'password reset')

    id = models.BigAutoField(primary_key=True)

    hash = models.CharField(max_length=255, db_index=True, unique=True)
    type = models.PositiveSmallIntegerField(choices=Types.choices)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now=True)

    # Annotations
    user_id: int

    class Meta:
        db_table = 'account_tokens'
        constraints = [models.UniqueConstraint(fields=['user_id', 'type'], name='uniq_token_type_per_user')]
