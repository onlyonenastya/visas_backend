from datetime import datetime
from django.db import models

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
    image = models.ImageField(verbose_name="Фото", upload_to="visas")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Виза"
        verbose_name_plural = "Визы"


class Order(models.Model):
    STATUS_CHOICES = [
        (1, "Зарегистрирован"),
        (2, "Проверяется"),
        (3, "Принято"),
        (4, "Отказано"),
        (5, "Удалено"),
    ]

    visas = models.ManyToManyField(Visa, verbose_name="Визы", null=True)

    status = models.IntegerField(verbose_name="Статус", default=1, choices=STATUS_CHOICES)
    date_created = models.DateField(verbose_name="Дата создания", default=datetime.now(tz=timezone.utc), blank=True, null=True)
    date_of_formation = models.DateField(verbose_name="Дата формирования", default=datetime.now(tz=timezone.utc), blank=True, null=True)
    date_complete = models.DateField(verbose_name="Дата завершения", blank=True, null=True)

    def __str__(self):
        return "Заказ №" + str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

