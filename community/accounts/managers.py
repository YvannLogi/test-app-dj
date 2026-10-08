from django.contrib.auth.models import BaseUserManager

class GlobalManager(BaseUserManager):
    def create_user(self, phone, full_name, email=None, password=None, **extra_fields):
        if not phone and full_name:
            raise ValueError("Phone and full name are required.")

        email = self.normalize_email(email) if email else email

        user = self.model(
            phone=phone,
            full_name=full_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, full_name, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Staff member must be True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Super-U must be True")

        return self.create_user(phone, full_name, email, password, **extra_fields)

