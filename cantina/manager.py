from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_escola(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_school=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_aluno(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, is_school=False, **extra_fields)
        user.set_password(password)
        user.save()
        return user