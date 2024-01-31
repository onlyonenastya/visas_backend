from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "users"


class Orders(models.Model):
    STATUS_CHOICES = [
        ("registered", "Зарегистрирован"),
        ("moderating", "Проверяется"),
        ("approved", "Принято"),
        ("denied", "Отказано"),
        ("deleted", "Удалено"),
    ]
    id = models.IntegerField(primary_key=True)
    status = models.CharField(
        max_length=255, blank=True, null=True, choices=STATUS_CHOICES
    )
    date_creation = models.DateField(blank=True, null=True)
    date_formation = models.DateField(blank=True, null=True)
    date_completion = models.DateField(blank=True, null=True)
    user = models.ForeignKey("Users", models.DO_NOTHING, blank=True, null=True)
    moderator = models.ForeignKey(
        "Users",
        models.DO_NOTHING,
        related_name="orders_moderator_set",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "orders"


class OrdersVises(models.Model):
    id = models.IntegerField(primary_key=True)
    order = models.ForeignKey(Orders, models.DO_NOTHING, blank=True, null=True)
    vise = models.ForeignKey("Vises", models.DO_NOTHING, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "orders_vises"


class Vises(models.Model):
    STATUS_CHOICES = [
        ("enabled", "Есть"),
        ("deleted", "Удалена"),
    ]
    id = models.IntegerField(primary_key=True)
    status = models.CharField(
        max_length=255, blank=True, null=True, choices=STATUS_CHOICES
    )
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
