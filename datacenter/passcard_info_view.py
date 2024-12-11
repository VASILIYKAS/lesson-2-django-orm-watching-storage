from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits_for_passcard = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []

    for visit in visits_for_passcard:
        duration_seconds = visit.get_duration()
        is_strange = visit.is_visit_long(60)

        this_passcard_visits.append(
            {
                'entered_at': visit.entered_at,
                'duration': visit.format_duration(duration_seconds),
                'is_strange': is_strange
            }
        )

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
