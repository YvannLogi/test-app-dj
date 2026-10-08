from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

phone_regex = RegexValidator(
    regex=r'^(01|05|07)\d{8}$',
    message="This number phone is not allowed."
)

# 1. Validateur d'extension (PNG, WEBP, PDF uniquement)
validate_file_extension = FileExtensionValidator(
    allowed_extensions=['png', 'webp'],
    message="Extension non autorisée. Seuls les formats PNG et WEBP sont acceptés."
)

# 2. Validateur de taille (Ex: max 5 Mo)
def validate_file_size(value):
    max_size_mb = 5
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f"Le fichier est trop volumineux. La taille maximale autorisée est de {max_size_mb} Mo."
        )
