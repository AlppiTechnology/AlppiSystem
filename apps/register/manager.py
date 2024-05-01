from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, registration, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not registration:
            raise ValueError(_("The registration must be set"))
        user = self.model(registration=registration, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, registration, password, **extra_fields):
        """
        Create and save a SuperUser with the given registration and password.
        """
        extra_fields.setdefault("cpf", '02353336035')
        extra_fields.setdefault("username", 'Patrick Berlatto Piccini')
        extra_fields.setdefault("phone", '54990293378')
        extra_fields.setdefault("email", 'patrick@piccini.com')
        extra_fields.setdefault("sex", 'M')
        extra_fields.setdefault("birth_date", '1999-12-14')
        extra_fields.setdefault("edited", '2024-01-30 00:00:00')
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)


        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(registration, password, **extra_fields)