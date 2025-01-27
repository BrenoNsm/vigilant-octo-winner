from django.apps import AppConfig
from django.contrib.auth import get_user_model

class SiteSeampConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'siteSeamp'

    def ready(self):
        from django.db.utils import OperationalError  # Import interno para evitar erros
        from django.db import IntegrityError  # Para tratar problemas na criação do usuário

        try:
            # Usa get_user_model para obter o modelo de usuário dinamicamente
            User = get_user_model()
            ai_user, created = User.objects.get_or_create(
                username="AI-Dito",
                defaults={"is_active": False, "first_name": "IA-Dito", "last_name": "G01"}
            )
            if created:
                print("Usuário Gemini (IA) criado com sucesso.")
        except (OperationalError, IntegrityError):
            # Evita erros se o banco ainda não estiver configurado ou se houver duplicatas
            print("Usuário Gemini não foi criado. Banco de dados ainda não está pronto.")
