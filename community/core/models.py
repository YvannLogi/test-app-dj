from django.db import models
from django.urls import reverse
from common.mixins import SlugMixin, Stamp
from accounts.models import Rabbin, Member
from django.contrib.auth import get_user_model

BaseUser = get_user_model()


class Temple(SlugMixin):
    """Communauté / temple dirigé par un rabbin."""
    
    name = models.CharField(
        "Nom du temple",
        max_length=200,
        unique=True,
    )
    address = models.CharField(
        "Adresse",
        max_length=200,
    )
    rabbin = models.OneToOneField(
        Rabbin,
        on_delete=models.RESTRICT,
        related_name="temple",
        verbose_name="Rabbin",
    )

    class Meta:
        verbose_name = "Temple"
        verbose_name_plural = "Temples"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["rabbin"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.rabbin.user.full_name}"

    def get_absolute_url(self):
        return reverse('core:temple-detail', args=[self.slug])


class EventType(SlugMixin):
    name = models.CharField("Catégorie d'un évènement", max_length=200, unique=True, db_index=True)

    def __str__(self): return self.name

    class Meta:
        verbose_name = "Type d'evenement"
        verbose_name_plural = "Types d'evenements"
        ordering = ['name']


class Event(SlugMixin):
    """Événement organisé par une communauté."""
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(
        "Titre",
        max_length=200,
    )
    content = models.TextField(
        "Description",
        blank=True,
    )
    date = models.DateTimeField(
        "Date et heure",
    )
    temple = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name="Temple",
    )

    is_verified = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["date"]),
            models.Index(fields=["temple", "date"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.date:%d/%m/%Y %H:%M}"
    

    def get_absolute_url(self):
        return reverse('core:event-detail', args=[self.slug])


class MemberRequest(Stamp):
    """Demande d'adhésion d'un utilisateur à une communauté."""

    adherent = models.ForeignKey(
        BaseUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="member_requests",
        verbose_name="Demandeur",
    )

    guest_full_name = models.CharField(
        "Nom complet",
        max_length=150,
        blank=True,
    )

    guest_phone = models.CharField(
        "Téléphone",
        max_length=30,
        blank=True,
    )

    guest_address = models.CharField(
        "Adresse",
        max_length=255,
        blank=True,
    )

    temple = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE,
        related_name="member_requests",
        verbose_name="Temple",
    )

    class Meta:
        verbose_name = "Demande d'adhésion"
        verbose_name_plural = "Demandes d'adhésion"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["adherent"]),
            models.Index(fields=["temple"]),
            models.Index(fields=["temple", "adherent"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["adherent", "temple"],
                name="unique_member_request_per_temple",
            ),
        ]


    def __str__(self):
        by_user = self.adherent.full_name if self.adherent else self.guest_full_name
        return f"Request to join {self.temple.name} temple by {by_user}"



class RecommendationLetter(Stamp):
    """Lettre de recommandation d'un membre de la communauté."""

    member = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recommendation_letters",
        verbose_name="Membre",
    )
    approved_by = models.ForeignKey(
        Rabbin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_recommendation_letters",
        verbose_name="Approuvée par",
        limit_choices_to={
            "user__role": BaseUser.Role.RABBIN,
        },
    )

    class Meta:
        verbose_name = "Lettre de recommandation"
        verbose_name_plural = "Lettres de recommandation"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["member"]),
            models.Index(fields=["approved_by"]),
        ]


class BlogCategory(SlugMixin):
    name = models.CharField("Categorie", max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog catégorie"
        verbose_name_plural = "Blogs catégories"


class BlogPost(SlugMixin):
    """Publication du blog d'une communauté."""
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name="blog_post")

    title = models.CharField(
        "Titre",
        max_length=200,
    )
    content = models.TextField(
        "Contenu",
        blank=True,
    )
    temple = models.ForeignKey(
        Temple,
        on_delete=models.CASCADE,
        related_name="blog_posts",
        verbose_name="Temple",
    )

    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Article de blog"
        verbose_name_plural = "Articles de blog"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["temple"]),
            models.Index(fields=["temple", "created_at"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogpost-detail', kwargs={
            'cat_slug': self.category.slug,
            'slug': self.slug
        })


    @property
    def blog_lists(self):
        return self.is_published and self.temple.name if self.temple else "Synagogue"
