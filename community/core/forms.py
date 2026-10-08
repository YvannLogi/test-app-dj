from django import forms
from django.core.exceptions import ValidationError
from .models import MemberRequest
import re

INPUT_CLASSES = (
    "w-full px-4 py-2 rounded-lg border border-gray-300 "
    "focus:outline-none focus:ring-2 focus:ring-[#0802C] "
    "focus:border-[#0802C]"
)


class MemberRequestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Classes CSS communes
        self.fields["temple"].widget.attrs.update({"class": INPUT_CLASSES})
        self.fields["guest_full_name"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "placeholder": "Ex: Kouassi Jean"
        })
        self.fields["guest_phone"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "type": "tel",
            "placeholder": "Ex: 0700000000"
        })
        self.fields["guest_address"].widget.attrs.update({
            "class": INPUT_CLASSES,
            "placeholder": "Ex: Cocody, Abidjan"
        })

        # Utilisateur connecté
        if user and user.is_authenticated:
            self.fields["guest_full_name"].initial = getattr(user, "full_name", "")
            self.fields["guest_phone"].initial = getattr(user, "phone", "")
            self.fields["guest_address"].initial = getattr(user, "address", "")
            
            self.fields["guest_full_name"].required = False
            self.fields["guest_phone"].required = False
            self.fields["guest_address"].required = False
        else:
            self.fields["guest_full_name"].required = True
            self.fields["guest_phone"].required = True
            self.fields["guest_address"].required = True

    def clean_guest_full_name(self):
        name = self.cleaned_data.get("guest_full_name", "")
        if name:
            # Vérification stricte : interdire les chiffres
            if any(char.isdigit() for char in name):
                raise ValidationError("Le nom complet ne doit pas contenir de chiffres.")
            
            # Vérification anti-emojis (plage Unicode des emojis)
            emoji_pattern = re.compile(
                r"[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u1f300-\u1f5ff]|[\u1f600-\u1f64f]|[\u1f680-\u1f6ff]|[\u2650-\u267f]",
                re.UNICODE
            )
            if emoji_pattern.search(name):
                raise ValidationError("Les emojis ne sont pas autorisés dans le nom.")
        return name

    def clean_guest_phone(self):
        phone = self.cleaned_data.get("guest_phone", "")
        if phone:
            # Nettoyer les espaces, tirets, ou le signe + au début si l'utilisateur en met
            cleaned_phone = phone.strip().replace(" ", "").replace("-", "").replace("+", "")
            
            # Vérifier que le reste est strictement composé de chiffres
            if not cleaned_phone.isdigit():
                raise ValidationError("Le numéro de téléphone doit contenir uniquement des chiffres.")
            
            if len(cleaned_phone) < 8 or len(cleaned_phone) > 15:
                raise ValidationError("Le format du numéro de téléphone est invalide.")
                
        return phone

    class Meta:
        model = MemberRequest
        fields = (
            "temple",
            "guest_full_name",
            "guest_phone",
            "guest_address",
        )
