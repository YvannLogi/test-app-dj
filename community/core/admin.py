from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from .models import (
    Temple,
    EventType,
    Event,
    MemberRequest,
    RecommendationLetter,
    BlogCategory,
    BlogPost,
)


# ============================================================
# EVENT TYPE
# ============================================================

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "events_count",
    )

    # exclude = ('slug',)

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                _events_count=Count("events", distinct=True)
            )
        )

    @admin.display(
        description="Événements",
        ordering="_events_count",
    )
    def events_count(self, obj):
        return obj._events_count


# ============================================================
# TEMPLE
# ============================================================

@admin.register(Temple)
class TempleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rabbin_name",
        "address",
        "events_count",
        "members_requests_count",
    )

    search_fields = (
        "name",
        "address",
        "rabbin__user__full_name",
        "rabbin__user__phone",
    )

    list_filter = (
        "rabbin__user__role",
    )

    autocomplete_fields = (
        "rabbin",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )

    list_per_page = 25

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "rabbin__user",
            )
            .annotate(
                _events_count=Count(
                    "events",
                    distinct=True,
                ),
                _member_requests_count=Count(
                    "member_requests",
                    distinct=True,
                ),
            )
        )

    @admin.display(
        description="Rabbin",
        ordering="rabbin__user__full_name",
    )
    def rabbin_name(self, obj):
        return obj.rabbin.user.full_name

    @admin.display(
        description="Événements",
        ordering="_events_count",
    )
    def events_count(self, obj):
        return obj._events_count

    @admin.display(
        description="Demandes",
        ordering="_member_requests_count",
    )
    def members_requests_count(self, obj):
        return obj._member_requests_count


# ============================================================
# EVENT
# ============================================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event_type",
        "temple",
        "date",
        "is_past",
    )

    list_filter = (
        "event_type",
        "temple",
        "date",
    )

    search_fields = (
        "title",
        "content",
        "temple__name",
        "event_type__name",
    )

    autocomplete_fields = (
        "event_type",
        "temple",
    )

    date_hierarchy = "date"

    prepopulated_fields = {
        "slug": ("title",),
    }

    ordering = (
        "-date",
    )

    list_per_page = 25

    list_select_related = (
        "event_type",
        "temple",
    )

    @admin.display(
        boolean=True,
        description="Passé",
    )
    def is_past(self, obj):
        from django.utils import timezone

        return obj.date < timezone.now()


# ============================================================
# MEMBER REQUEST
# ============================================================

@admin.register(MemberRequest)
class MemberRequestAdmin(admin.ModelAdmin):
    list_display = (
        "adherent_name",
        "adherent_phone",
        "temple",
        "created_at",
    )

    list_filter = (
        "temple",
        "created_at",
    )

    search_fields = (
        "adherent__full_name",
        "adherent__phone",
        "adherent__email",
        "temple__name",
    )

    autocomplete_fields = (
        "adherent",
        "temple",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    list_select_related = (
        "adherent",
        "temple",
    )

    @admin.display(
        description="Demandeur",
        ordering="adherent__full_name",
    )
    def adherent_name(self, obj):
        if not obj.adherent:
            return obj.guest_full_name

        return obj.adherent.full_name

    @admin.display(
        description="Téléphone",
        ordering="adherent__phone",
    )
    def adherent_phone(self, obj):
        if not obj.adherent:
            return obj.guest_phone

        return obj.adherent.phone


# ============================================================
# RECOMMENDATION LETTER
# ============================================================

@admin.register(RecommendationLetter)
class RecommendationLetterAdmin(admin.ModelAdmin):
    list_display = (
        "member_name",
        "approved_by_name",
        "created_at",
    )

    list_filter = (
        "approved_by",
        "created_at",
    )

    search_fields = (
        "member__user__full_name",
        "member__user__phone",
        "member__matricule",
        "approved_by__user__full_name",
    )

    autocomplete_fields = (
        "member",
        "approved_by",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    list_select_related = (
        "member__user",
        "approved_by__user",
    )

    @admin.display(
        description="Membre",
        ordering="member__user__full_name",
    )
    def member_name(self, obj):
        if not obj.member:
            return "Membre supprimé"

        return obj.member.user.full_name

    @admin.display(
        description="Approuvée par",
        ordering="approved_by__user__full_name",
    )
    def approved_by_name(self, obj):
        if not obj.approved_by:
            return "Non approuvée"

        return obj.approved_by.user.full_name


# ============================================================
# BLOG CATEGORY
# ============================================================

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "posts_count",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                _posts_count=Count(
                    "blog_post",
                    distinct=True,
                )
            )
        )

    @admin.display(
        description="Articles",
        ordering="_posts_count",
    )
    def posts_count(self, obj):
        return obj._posts_count


# ============================================================
# BLOG POST
# ============================================================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "temple",
        "created_at",
    )

    list_filter = (
        "category",
        "temple",
        "created_at",
    )

    search_fields = (
        "title",
        "content",
        "category__name",
        "temple__name",
    )

    autocomplete_fields = (
        "category",
        "temple",
    )

    prepopulated_fields = {
        "slug": ("title",),
    }

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    list_select_related = (
        "category",
        "temple",
    )