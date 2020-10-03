from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("Username not set")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_tutor(self, username, password=True, **extra_fields):
        extra_fields.setdefault('is_tutor', True)

        return self._create_user(username, password, **extra_fields)

    def create_student(self, username, password=True, **extra_fields):
        extra_fields.setdefault('is_student', True)

        return self._create_user(username, password, **extra_fields)

    def create_user(self, username, password=True, **extra_fields):
        extra_fields.setdefault('is_admin', False)

        return self._create_user(username, password, **extra_fields)
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(username, password, **extra_fields)
