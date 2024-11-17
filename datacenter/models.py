from django.db import models
from django.utils.timezone import localtime


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
        current_time = localtime()
        enter = self.entered_at
        enter_time = localtime(enter)
        delta = current_time - enter_time
        duration = delta.total_seconds()
        return duration

    def format_duration(self):
        hours = self // 3600
        minutes = (self % 3600) // 60
        format_time = f'{int(hours)}:{int(minutes):02}:00'
        return format_time

    def is_visit_long(self, minutes=60):
        if self.leaved_at is None:
            return 'Ещё внутри'
        enter_time = localtime(self.entered_at)
        leaved_time = localtime(self.leaved_at)
        delta = leaved_time - enter_time
        duration_seconds = delta.total_seconds()
        duration_in_minutes = duration_seconds // 60
        return duration_in_minutes >= minutes