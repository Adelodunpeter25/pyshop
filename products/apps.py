from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        # Register signal to hide recent actions bar after apps are loaded
        from admin_interface.models import Theme
        from django.db.models.signals import post_migrate
        from django.dispatch import receiver

        @receiver(post_migrate)
        def hide_recent_actions(sender, **kwargs):
            Theme.objects.all().update(recent_actions_visible=False)
