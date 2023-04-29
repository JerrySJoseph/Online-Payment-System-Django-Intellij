from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet'


    def ready(self):
        # import signals module to be able to listen to user_creation events
        import wallet.signals
