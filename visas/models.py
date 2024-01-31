from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from datetime import date
from django.utils import timezone


class Visa(models.Model):
    STATUS_CHOICES = [
        (1, "Действует"),
        (2, "Удалена"),
    ]

    name = models.CharField(verbose_name="Название", default="Название визы", max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name="Описание",default="Описание визы", blank=True, null=True)
    status = models.IntegerField(verbose_name="Статус", default=1, choices=STATUS_CHOICES)
    country = models.CharField(verbose_name="Страны", default="Европа, Азия, Америка", max_length=255, blank=True, null=True)
    price = models.IntegerField(verbose_name="Цена", default=5000, blank=True, null=True)
    duration = models.IntegerField(verbose_name="Срок действия", default=5, blank=True, null=True)
    image = models.CharField(verbose_name="Фото",max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Виза"
        verbose_name_plural = "Визы"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    is_moderator = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Order(models.Model):

    STATUS_CHOICES = [
        (1, "Зарегистрирован"),
        (2, "Проверяется"),
        (3, "Принято"),
        (4, "Отказано"),
        (5, "Удалено"),
    ]

    # первая версия ассинхронного сервиса
    delivery_date = models.IntegerField(verbose_name="Время выполнение заказа (в днях)", blank=True, null=True)
    
    violation = models.CharField(verbose_name="Нарушения", max_length=255, blank=True, null=True)


    visas = models.ManyToManyField(Visa, verbose_name="Визы", null=True)

    status = models.IntegerField(verbose_name="Статус", default=1, choices=STATUS_CHOICES)
    date_created = models.DateField(verbose_name="Дата создания", default=date.today, blank=True, null=True)
    date_of_formation = models.DateField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateField(verbose_name="Дата завершения", blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, related_name='user')
    moderator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Модератор", null=True, related_name='moderator')
    
    def __str__(self):
        return "Заказ №" + str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

