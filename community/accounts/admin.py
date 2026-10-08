from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import BaseUser, Member, Rabbin


# ---------------------------------------------------------------------------
# Formulaires : adaptés à un modèle qui utilise `phone` comme identifiant
# ---------------------------------------------------------------------------
class BaseUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = BaseUser
        fields = ("phone", "full_name", "email", "role")


class BaseUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = BaseUser
        fields = "__all__"


# ---------------------------------------------------------------------------
# BaseUser : hérite de UserAdmin => mot de passe haché (password1 / password2)
# ---------------------------------------------------------------------------
@admin.register(BaseUser)
class BaseUserAdmin(UserAdmin):
    add_form = BaseUserCreationForm
    form = BaseUserChangeForm
    model = BaseUser

    list_display = (
        "full_name",
        "phone",
        "email",
        "role",
        "is_active",
    )
    search_fields = (
        "full_name",
        "phone",
        "email",
    )
    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )
    ordering = ("full_name",)
    list_per_page = 25

    # Page de modification
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Informations personnelles", {"fields": ("full_name", "email", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates importantes", {"fields": ("last_login",)}),
    )

    # Page d'ajout
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "full_name",
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


# ---------------------------------------------------------------------------
# Rabbin
# ---------------------------------------------------------------------------
@admin.register(Rabbin)
class RabbinAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "role",
    )
    search_fields = (
        "user__full_name",
        "user__phone",
        "user__email",
    )
    list_select_related = ("user",)
    ordering = ("user__full_name",)
    autocomplete_fields = ("user",)  # nécessite search_fields sur BaseUserAdmin
    list_per_page = 25

    @admin.display(description="Nom complet", ordering="user__full_name")
    def full_name(self, obj):
        return obj.user.full_name

    @admin.display(description="Téléphone", ordering="user__phone")
    def phone(self, obj):
        return obj.user.phone

    @admin.display(description="Rôle", ordering="user__role")
    def role(self, obj):
        return obj.user.role


# ---------------------------------------------------------------------------
# Member
# ---------------------------------------------------------------------------
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone",
        "matricule",
        "temple",  # <-- Ajouté ici pour l'afficher dans la liste
    )
    search_fields = (
        "user__full_name",
        "user__phone",
        "user__email",
        "matricule",
        "temple__name",  # <-- Optionnel : permet de rechercher par nom de temple
    )
    list_select_related = ("user", "temple")  # <-- Ajout de "temple" pour optimiser les requêtes SQL
    ordering = ("user__full_name",)
    autocomplete_fields = ("user", "temple")  # <-- Permet une recherche fluide si tu as beaucoup de temples
    list_per_page = 25

    @admin.display(description="Nom complet", ordering="user__full_name")
    def full_name(self, obj):
        return obj.user.full_name

    @admin.display(description="Téléphone", ordering="user__phone")
    def phone(self, obj):
        return obj.user.phone