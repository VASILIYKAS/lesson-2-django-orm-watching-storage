from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Visit


def storage_information_view(request):
    # Программируем здесь
    visits = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []

    for i in visits:
        name = i.passcard.owner_name
        enter = i.entered_at
        enter_time = localtime(enter)
        visit = Visit.get_duration(i)
        duration = Visit.format_duration(visit)

        non_closed_visits.append(
            {
                'who_entered': name,
                'entered_at': enter_time,
                'duration': duration
            }
        )


    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
