from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BaseUser, Rabbin, Member

@receiver(post_save, sender=BaseUser)
def create_user_profile(sender, instance, created, **kwargs):
    # On s'assure de ne faire l'association qu'à la création
    if not created:
        return

    # Création du profil selon le rôle choisi
    if instance.role == BaseUser.Role.RABBIN:
        Rabbin.objects.get_or_create(user=instance)
        
    elif instance.role == BaseUser.Role.MEMBER:
        Member.objects.get_or_create(user=instance)