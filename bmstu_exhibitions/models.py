from django.db import models


class Orders(models.Model):
    STATUS_CHOICES = [
        ("registered", "Зарегистрирован"),
        ("moderating", "Проверяется"),
        ("approved", "Принято"),
        ("denied", "Отказано"),
        ("deleted", "Удалено"),
    ]
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    date_creation = models.DateField(blank=True, null=True)
    date_formation = models.DateField(blank=True, null=True)
    date_completion = models.DateField(blank=True, null=True)
    id_moderator = models.ForeignKey(
        "Users", models.DO_NOTHING, db_column="id_moderator", blank=True, null=True
    )
    id_user = models.ForeignKey(
        "Users",
        models.DO_NOTHING,
        db_column="id_user",
        related_name="orders_id_user_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "orders"


class OrdersVises(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING)
    vise = models.ForeignKey("Vises", models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "orders_vises"


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "users"


class Vises(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=255, decimal_places=0, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    specialist = models.CharField(max_length=255, blank=True, null=True)
    specialist_url = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)

    class Meta:
        db_table = "vises"
