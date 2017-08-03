from django_cron import CronJobBase, Schedule
from muni.munisystem.munisystem import MUNISystem
class updateRouteConfigs_Weekly(CronJobBase):
    RUN_EVERY_MINS = 10080

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)

    code = 'muni.munisystem.scheduler.updateRouteConfigs_Weekly'

    def do(self):
        MUNISystem.updateRouteConfigs()


