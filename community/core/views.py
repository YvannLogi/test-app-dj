from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Temple, Event, BlogPost
from .forms import MemberRequestForm
from django.core.exceptions import ObjectDoesNotExist


class HomeView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["temples"] = (
            Temple.objects
            .values("name", "address", "slug")
            .order_by("-created_at")[:3]
        )

        ctx["last_events"] = (
            Event.objects
            .select_related("event_type")
            .filter(is_verified=True)
            .values(
                "title",
                "date",
                "slug",
                "event_type__name",
            )
            .order_by("-date")[:3]
        )

        ctx["blogs"] = (
            BlogPost.objects
            .select_related("category")
            .filter(is_published=True)
            .values(
                "title",
                "slug",
                "category__name",
                "created_at",
            )
            .order_by("-created_at")[:3]
        )

        return ctx


""" lists """


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "core/blog-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).select_related(
            "category", "temple"
        )


class EventListView(ListView):
    model = Event
    template_name = "core/ev-list.html"
    context_object_name = "events"
    paginate_by = 3

    def get_queryset(self):
        return Event.objects.filter(is_verified=True).select_related(
            "event_type", "temple"
        )


class TempleListView(ListView):
    model = Temple
    template_name = "core/sy-list.html"
    context_object_name = "temples"

    def get_queryset(self):
        return Temple.objects.select_related("rabbin__user")


""" detail """
class TempleDetailView(DetailView):
    model = Temple
    template_name = "core/sy-detail.html"  # Adapte selon ton template
    context_object_name = "temple"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        is_member_of_this_temple = False
        user_has_temple = False

        if user.is_authenticated:
            member_profile = getattr(user, "member_profile", None)
            if member_profile:
                # L'utilisateur a un profil membre, a-t-il déjà un temple ?
                if member_profile.temple:
                    user_has_temple = True
                    # Est-ce que c'est CE temple-ci ?
                    if member_profile.temple == self.object:
                        is_member_of_this_temple = True

        context["is_user_member"] = is_member_of_this_temple
        context["user_has_temple"] = user_has_temple
        return context
    

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "core/ev-detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "event"

    def get_queryset(self):
        return Event.objects.select_related("event_type", "temple")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["related_events"] = (
            Event.objects.filter(
                event_type=self.object.event_type,
                is_verified=True,
            )
            .exclude(pk=self.object.pk)
            .select_related("event_type", "temple")
        )

        return ctx


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = "core/blog-detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "post"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).select_related(
            "category", "temple"
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["related_posts"] = (
            BlogPost.objects.filter(
                category=self.object.category,
                is_published=True,
            )
            .exclude(pk=self.object.pk)
            .select_related("category", "temple")
        )

        return ctx



""" request to join """
class MemberRequestSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "core/sy-request-success.html"


class MemberRequestFormCreateView(LoginRequiredMixin, CreateView):
    form_class = MemberRequestForm
    template_name = "core/sy-request_form.html"
    success_url = reverse_lazy("core:join-community-success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user and self.request.user.is_authenticated:
            form.instance.adherent = self.request.user
        return super().form_valid(form)

