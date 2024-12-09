from django.db import models
from django.utils.timezone import localtime

SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        if self.leaved_at is not None:
            exit_time = localtime(self.leaved_at)
        else:
            exit_time = localtime()

        enter_time = localtime(self.entered_at)
        delta = exit_time - enter_time
        duration = delta.total_seconds()
        return duration

    def format_duration(self, duration):
        hours = duration // SECONDS_IN_HOUR
        minutes = (duration % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
        format_time = f'{int(hours)}:{int(minutes):02}:00'
        return format_time

    def is_visit_long(self, minutes=60):
        if self.leaved_at is None:
            return 'Ещё внутри'

        duration_seconds = self.get_duration()
        duration_in_minutes = duration_seconds // 60
        return duration_in_minutes >= minutes

    def assess_visit_suspicion(self):
        minutes = Visit.get_duration(self) // 60
        if 60 <= minutes <= 120:
            return 'Да'
        elif minutes > 120:
            return 'Очень'
        else:
            return 'Нет'
