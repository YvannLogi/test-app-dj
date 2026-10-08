from django.db import models
from django.utils.text import slugify

class Stamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class SlugMixin(Stamp):
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            # On cherche dynamiquement si le modèle a un attribut 'name' ou 'title'
            source_value = getattr(self, 'name', None) or getattr(self, 'title', None)
            
            if source_value:
                base_slug = slugify(source_value)
                slug = base_slug
                counter = 1
                
                # Gestion de l'unicité pour éviter les doublons en base
                while self.__class__.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                self.slug = slug
                
        super().save(*args, **kwargs)
