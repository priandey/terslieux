import csv

from django.conf import global_settings
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
import weasyprint

from user.models import CustomUser
from location.models import Location, Status, VolunteerBase


def generate_pdf(request, slug):
    """
    :param slug: Slug for the location
    :return: Should return a pdf file with statuses data.
            !IMPORTANT! PDF is not a good call for this usage.
            TODO : Replace this view before 1.5 release
    """
    location = Location.objects.get(slug=slug)
    statuses = location.status.all()
    if request.user == location.moderator:
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
                                                       'global_opening': global_opening_duration})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename="statistic_{location.name}.pdf"'
        weasyprint.HTML(string=html).write_pdf(
            response
        )
        return response
    else:
        return HttpResponseForbidden("Vous n'avez pas accès à ces données")


def generate_csv(request, slug):
    """
    This view transmit ordered data about location statuses.
    :param slug: Slug for the location
    :return: Should return a CSV file
    """
    location = Location.objects.get(slug=slug)
    statuses = location.status.all()
    if request.user == location.moderator:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}-data.csv'.format(location.slug)
        writer = csv.writer(response, delimiter=";", dialect='excel')
        writer.writerow(
                ["Activite", "Details", "Date d'ouverture", "Date de fermeture", "Temps d'ouverture (secondes)"]
        )
        for status in statuses:
            writer.writerow(
                    [status.activity, status.description, status.open_date, status.close_date, status.open_time['total_seconds']]
            )
    else:
        response = HttpResponseForbidden("Vous n'avez pas accès à ces données")
    return response
