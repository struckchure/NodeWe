from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class HomeConfig(AppConfig):
    name = 'Home'
    verbose_name = _('Home')

    def ready(self):
        import Home.signals
