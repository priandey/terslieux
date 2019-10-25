from django.conf import global_settings
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
import weasyprint

from user.models import CustomUser
from location.models import Location, Status, VolunteerBase

def generate_pdf(request, slug):
    location = Location.objects.get(slug=slug)
    if request.user == location.moderator:
        statuses = location.status.all()
        # Calculating and formatting total opening duration
        global_opening_duration = int()
        for status in statuses:
            global_opening_duration += status.open_time['total_seconds']
        global_hours = global_opening_duration // 3600
        global_rest = global_opening_duration % 3600
        global_minutes = global_rest // 60
        global_opening_duration = '{} hours, {} minutes'.format(global_hours, global_minutes)
        # Rendering pdf
        html = render_to_string('statistic/pdf.html', {'statuses': statuses,
                                                        'global_opening':global_opening_duration})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="statistic_{location.name}.pdf"'
        weasyprint.HTML(string=html).write_pdf(
            response
        )
        return response
    else:
        return HttpResponseForbidden()
