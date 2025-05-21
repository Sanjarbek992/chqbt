from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from sorl.thumbnail import get_thumbnail
from django.urls import reverse_lazy



# Role tanlovlari
class Role(models.TextChoices):
    SUPERADMIN = 'superadmin', 'SuperAdmin'
    ADMIN = 'admin', 'Admin'
    MODERATOR = 'moderator', 'Moderator'
    TEACHER = 'teacher', 'Teacher'
    EMPLOYEE = 'employee', 'Employee'
    USER = 'user', 'User'


# Maxsus user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, role, pinfl, password=None):
        if not username:
            raise ValueError("Username talab qilinadi")
        if not pinfl or len(pinfl) != 14 or not pinfl.isdigit():
            raise ValueError("PINFL 14 raqamli va to'g'ri formatda bo'lishi kerak")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=role,
            pinfl=pinfl,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, pinfl, password=None):
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            role=Role.SUPERADMIN,
            pinfl=pinfl,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Asosiy foydalanuvchi modeli
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pinfl = models.CharField(max_length=14, unique=True, verbose_name="PINFL")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    profile_completed = models.BooleanField(default=False)
    is_verified_by_external_api = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'pinfl']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.get_full_name()} - {self.username}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    @property
    def is_superadmin(self):
        return self.role == Role.SUPERADMIN

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_teacher(self):
        return self.role == Role.TEACHER

    @property
    def is_employee(self):
        return self.role == Role.EMPLOYEE

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"


# Harbiy unvonlar
class MilitaryRank(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Harbiy unvon")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Harbiy unvon"
        verbose_name_plural = "Harbiy unvonlar"


# Foydalanuvchi profilingi
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=50, verbose_name="Otasining ismi", blank=True)
    profile_image = models.ImageField(upload_to="profile/", default='static/images/default_profile.png', blank=True)
    military_rank = models.ForeignKey(MilitaryRank, on_delete=models.SET_NULL, null=True, blank=True,
                                      verbose_name="Harbiy unvoni")
    department = models.CharField(max_length=255, blank=True, null=True, verbose_name="Muassasa yoki boshqarma")
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    passport_series = models.CharField(max_length=10, blank=True, null=True)
    GENDER_CHOICES = (
        ('male', 'Erkak'),
        ('female', 'Ayol'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    address = models.TextField(blank=True, null=True, verbose_name="Yashash manzili")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return '/static/images/default_profile.png'

    def image_thumbnail(self):
        if self.profile_image:
            return get_thumbnail(self.profile_image, '200x200', crop='center', quality=90).url
        return None

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.role})"

    def get_absolute_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def is_complete(self):
        required_fields = [self.jshir, self.birth_date, self.gender, self.school]
        return all(required_fields)
