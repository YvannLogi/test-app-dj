from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import RegisterForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist

BaseUser = get_user_model()

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        res = super().form_valid(form)

        user = self.object
        login(self.request, user)
        return res

    """ empêcher le user d'accéder au /register/ si connecté et le rédiriger vers la page d'accueil. """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')

        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.role == BaseUser.Role.RABBIN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context["rabbi_temple"] = None
        context["temple_members"] = []

        if user.is_superuser:
            # Gestion Super Admin si nécessaire
            pass
        elif hasattr(user, "rabbin") and user.rabbin:
            try:
                # Utilisation directe du related_name "temple"
                temple = user.rabbin.temple
                context["rabbi_temple"] = temple
                context["temple_members"] = temple.members.select_related("user").all()
            except ObjectDoesNotExist:
                # Le rabbin n'a pas encore de temple rattaché
                pass
                
        return context

