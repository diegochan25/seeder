from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import RelatedManager, ManyRelatedManager
    from apps.schemas.models import Schema


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, admin: bool = False, **kwargs):
        if not email:
            raise ValueError('The email field must be set')
        user = self.model(email=self.normalize_email(email), is_superuser=admin, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **kwargs):
        kwargs.pop('admin', None)
        return self._create_user(email, password, admin=False, **kwargs)

    def create_superuser(self, email: str, password: str, **kwargs):
        kwargs.pop('admin', None)
        return self._create_user(email, password, admin=True, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    password = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Annotations
    userrole_set: 'ManyRelatedManager[RoleAssignment]'
    accounttoken_set: 'RelatedManager[AccountToken]'
    schema_set: 'RelatedManager[Schema]'

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def initials(self) -> str:
        initials = ''
        if self.first_name:
            initials += self.first_name[0].upper()
        if self.last_name:
            initials += self.last_name[0].upper()
        return initials

    class Meta:
        db_table = 'users'


class RoleAssignment(models.Model):
    pk = models.CompositePrimaryKey('user_id', 'role_id')

    user = models.ForeignKey('User', on_delete=models.CASCADE, db_index=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'role_assignments'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    permissions = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'roles'


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
