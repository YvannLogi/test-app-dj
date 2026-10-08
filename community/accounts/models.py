import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from common.mixins import Stamp
from common.validators import (
    phone_regex,
    validate_file_extension,
    validate_file_size,
)

from .managers import GlobalManager


class BaseUser(AbstractUser, Stamp):
    """Utilisateur principal de la plateforme."""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Super-utilisateur"
        RABBIN = "RABBIN", "Rabbin"
        MEMBER = "MEMBER", "Membre"

    username = None

    phone = models.CharField(
        "Téléphone",
        max_length=10,
        unique=True,
        validators=[phone_regex],
    )
    role = models.CharField(
        "Rôle",
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
        db_index=True,
    )
    full_name = models.CharField(
        "Nom complet",
        max_length=200,
    )
    address = models.CharField(
        "Adresse",
        max_length=200,
        blank=True,
    )
    email = models.EmailField(
        "Courriel",
        max_length=200,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        "Actif",
        default=True,
    )

    objects = GlobalManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["full_name"]),
            models.Index(fields=["role"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


class Rabbin(Stamp):
    """Profil professionnel d'un rabbin."""

    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="rabbin",
        verbose_name="Utilisateur",
    )
    avatar = models.ImageField(
        "Photo de profil",
        upload_to="avatars/rabbins/",
        validators=[
            validate_file_extension,
            validate_file_size,
        ],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Rabbin"
        verbose_name_plural = "Rabbins"
        ordering = ["user__full_name"]
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return self.user.full_name


class Member(Stamp):
    """Profil communautaire d'un membre."""

    user = models.OneToOneField(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="member_profile",
        verbose_name="Utilisateur",
    )
    matricule = models.UUIDField(
        "Matricule",
        unique=True,
        default=uuid.uuid4,
        editable=False,
        max_length=10
    )

    temple = models.ForeignKey(
        "core.Temple",  # Remplace par ton application si nécessaire
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
        verbose_name="Communauté / Temple",
    )

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"
        ordering = ["user__full_name"]
        indexes = [
            models.Index(fields=["matricule"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.matricule}"