from django.apps import AppConfig
from munisystem.munisystem import MUNISystem

class MUNIConfig(AppConfig):
    name = 'muni'
    verbose_name = "MUNIbook"
    def ready(self):
        MUNISystem.updateRouteConfigs()
