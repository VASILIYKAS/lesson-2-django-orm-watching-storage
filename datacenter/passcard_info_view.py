from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.all()[0]
    # Программируем здесь
    get_passcode = get_object_or_404(Passcard, passcode=passcode)
    visits_for_passcard = Visit.objects.filter(passcard=get_passcode)
    this_passcard_visits = []

    for i in visits_for_passcard:
        enter_time = i.entered_at
        leaved_time = i.leaved_at
        delta = leaved_time - enter_time
        duration_seconds = delta.total_seconds()
        strange = Visit.is_visit_long(i, 60)

        this_passcard_visits.append(
            {
            'entered_at': enter_time,
            'duration': Visit.format_duration(duration_seconds),
            'is_strange': strange
        }
        )

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
